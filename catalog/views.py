from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout as auth_logout, update_session_auth_hash
from .models import Product, Category, Region, City, ProductImage, UserProfile, SEOPage
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProductForm, UserProfileForm, CustomPasswordChangeForm, DeleteAccountForm, ContactForm
from django.conf import settings

from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
@require_http_methods(["GET", "POST"])
def logout(request):
    auth_logout(request)
    return redirect('catalog:product_list')

def category_redirect(request):
    """Redirect old category URLs (?parent_category=ID or ?category=ID) to new slug-based URLs."""
    from django.http import HttpResponsePermanentRedirect
    
    category_id = request.GET.get('parent_category') or request.GET.get('category')
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            if category.slug:
                return HttpResponsePermanentRedirect(category.get_absolute_url())
        except Category.DoesNotExist:
            pass
    
    # Fallback to product list if category not found or no slug
    return redirect('catalog:product_list')

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        """Redirect query param URLs to SEO-friendly slug-based URLs."""
        from django.http import HttpResponsePermanentRedirect
        
        # Check filters
        parent_category_id = request.GET.get('parent_category')
        category_id = request.GET.get('category')
        region_id = request.GET.get('region')
        city_id = request.GET.get('city')
        
        # Get effective category (subcategory has priority)
        cat_id = category_id if category_id else parent_category_id
        
        # Build filter params (exclude empty, page, sort, search, seller_type, sells_to)
        filter_params = {k: v for k, v in request.GET.items() 
                        if v and k not in ['page', 'sort', 'search', 'seller_type', 'sells_to']}
        
        # Remove parent_category if category exists
        if category_id and 'parent_category' in filter_params:
            filter_params.pop('parent_category')
        
        # Remove region if city exists
        if city_id and 'region' in filter_params:
            filter_params.pop('region')
        
        # Only redirect if there are location/category filters
        if not filter_params:
            return super().get(request, *args, **kwargs)
        
        try:
            # Category + City combination
            if cat_id and city_id:
                category = Category.objects.get(id=cat_id)
                city = City.objects.get(id=city_id)
                if category.slug and city.slug:
                    new_url = f"/{category.slug}/{city.slug}/"
                    # Preserve other params (page, sort, search, etc.)
                    query_params = []
                    for key in ['page', 'sort', 'search', 'seller_type']:
                        value = request.GET.get(key)
                        if value:
                            query_params.append(f"{key}={value}")
                    if query_params:
                        new_url += "?" + "&".join(query_params)
                    return HttpResponsePermanentRedirect(new_url)
            
            # Category + Region combination
            elif cat_id and region_id:
                category = Category.objects.get(id=cat_id)
                region = Region.objects.get(id=region_id)
                if category.slug and region.slug:
                    new_url = f"/{category.slug}/region/{region.slug}/"
                    # Preserve other params
                    query_params = []
                    for key in ['page', 'sort', 'search', 'seller_type']:
                        value = request.GET.get(key)
                        if value:
                            query_params.append(f"{key}={value}")
                    if query_params:
                        new_url += "?" + "&".join(query_params)
                    return HttpResponsePermanentRedirect(new_url)
            
            # Single filter redirects (only if exactly one filter)
            elif len(filter_params) == 1:
                # Category only
                if cat_id:
                    category = Category.objects.get(id=cat_id)
                    if category.slug:
                        return HttpResponsePermanentRedirect(category.get_absolute_url())
                
                # City only
                elif city_id:
                    city = City.objects.get(id=city_id)
                    if city.slug and city.region.slug:
                        return HttpResponsePermanentRedirect(city.get_absolute_url())
                
                # Region only
                elif region_id:
                    region = Region.objects.get(id=region_id)
                    if region.slug:
                        return HttpResponsePermanentRedirect(region.get_absolute_url())
        
        except (Category.DoesNotExist, City.DoesNotExist, Region.DoesNotExist, ValueError):
            pass
        
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        from django.utils import timezone
        from django.db.models import Q
        from django.db.models.functions import Lower
        
        # Филтрирай само активни обяви, които не са изтекли (по-нови от 30 дни)
        expiry_date = timezone.now() - timezone.timedelta(days=30)
        queryset = Product.objects.filter(is_active=True, created_at__gte=expiry_date)
        
        # Търсене по ключова дума (case-insensitive с Lower за кирилица)
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            search_lower = search_query.lower()
            queryset = queryset.annotate(
                title_lower=Lower('title'),
                description_lower=Lower('description'),
                category_name_lower=Lower('category__name'),
                city_name_lower=Lower('city__name'),
                region_name_lower=Lower('city__region__name')
            ).filter(
                Q(title_lower__contains=search_lower) | 
                Q(description_lower__contains=search_lower) |
                Q(category_name_lower__contains=search_lower) |
                Q(city_name_lower__contains=search_lower) |
                Q(region_name_lower__contains=search_lower)
            )
        
        # Филтриране по категория или подкатегория
        category_id = self.request.GET.get('category')
        parent_category_id = self.request.GET.get('parent_category')
        
        if category_id:
            # Ако има подкатегория, филтрирай само по нея
            queryset = queryset.filter(category_id=category_id)
        elif parent_category_id:
            # Ако има само главна категория, филтрирай по всички нейни подкатегории
            subcategories = Category.objects.filter(parent_id=parent_category_id)
            queryset = queryset.filter(category__in=subcategories)

        # Филтриране по област/населено място
        city_id = self.request.GET.get('city')
        region_id = self.request.GET.get('region')
        
        if city_id:
            # Ако има град, филтрирай по него
            queryset = queryset.filter(city_id=city_id)
        elif region_id:
            # Ако има само област, филтрирай по всички градове в нея
            cities = City.objects.filter(region_id=region_id)
            queryset = queryset.filter(city__in=cities)
        
        # Филтриране по тип продавач
        seller_type = self.request.GET.get('seller_type')
        if seller_type:
            queryset = queryset.filter(seller_type=seller_type)
        
        # Филтриране по "Продава на" (multi-select)
        sells_to = self.request.GET.getlist('sells_to')
        if sells_to:
            # Филтър за JSONField - продуктът трябва да има поне една от избраните опции
            from django.db.models import Q
            sells_to_filter = Q()
            for option in sells_to:
                sells_to_filter |= Q(sells_to__contains=[option])
            queryset = queryset.filter(sells_to_filter)
        
        # Сортиране
        sort_by = self.request.GET.get('sort', '-created_at')
        
        valid_sorts = {
            '-created_at': '-created_at',  # Най-нови
            'created_at': 'created_at',    # Най-стари
            'price': 'price',              # Цена: ниска към висока
            '-price': '-price'             # Цена: висока към ниска
        }
        
        if sort_by in valid_sorts:
            queryset = queryset.order_by(valid_sorts[sort_by])
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Показвай само главни категории (без родител)
        context['categories'] = Category.objects.filter(parent__isnull=True)
        context['regions'] = Region.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['selected_parent_category'] = self.request.GET.get('parent_category')
        context['selected_region'] = self.request.GET.get('region')
        context['selected_city'] = self.request.GET.get('city')
        context['selected_seller_type'] = self.request.GET.get('seller_type')
        context['selected_sells_to'] = self.request.GET.getlist('sells_to')
        context['seller_type_choices'] = Product.SELLER_TYPE_CHOICES
        context['sells_to_choices'] = Product.SELLS_TO_CHOICES
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_by'] = self.request.GET.get('sort', '-created_at')
        return context


class CategoryCityProductListView(ListView):
    """
    SEO-friendly URL view for combined category + city filters.
    Handles URLs like: /meso/sofia/ instead of ?parent_category=123&city=456
    """
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        from django.utils import timezone
        from django.db.models import Q
        from django.db.models.functions import Lower
        from django.http import Http404
        
        # Get category and city from URL slugs
        category_slug = self.kwargs.get('category_slug')
        city_slug = self.kwargs.get('city_slug')
        
        # Look up category by slug
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404(f"Категория '{category_slug}' не съществува")
        
        # Look up city by slug
        try:
            city = City.objects.get(slug=city_slug)
        except City.DoesNotExist:
            raise Http404(f"Град '{city_slug}' не съществува")
        
        # Store for use in context
        self.category = category
        self.city = city
        
        # Filter active products within 30 days
        expiry_date = timezone.now() - timezone.timedelta(days=30)
        queryset = Product.objects.filter(is_active=True, created_at__gte=expiry_date)
        
        # Apply category filter (check if parent or subcategory)
        if category.is_parent():
            # Main category - filter by all subcategories
            subcategories = Category.objects.filter(parent=category)
            queryset = queryset.filter(category__in=subcategories)
        else:
            # Subcategory - filter directly
            queryset = queryset.filter(category=category)
        
        # Apply city filter
        queryset = queryset.filter(city=city)
        
        # Search query (optional)
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            search_lower = search_query.lower()
            queryset = queryset.annotate(
                title_lower=Lower('title'),
                description_lower=Lower('description')
            ).filter(
                Q(title_lower__contains=search_lower) | 
                Q(description_lower__contains=search_lower)
            )
        
        # Seller type filter (optional)
        seller_type = self.request.GET.get('seller_type')
        if seller_type:
            queryset = queryset.filter(seller_type=seller_type)
        
        # Sells to filter (optional)
        sells_to = self.request.GET.getlist('sells_to')
        if sells_to:
            from django.db.models import Q
            sells_to_filter = Q()
            for option in sells_to:
                sells_to_filter |= Q(sells_to__contains=[option])
            queryset = queryset.filter(sells_to_filter)
        
        # Sorting
        sort_by = self.request.GET.get('sort', '-created_at')
        valid_sorts = {
            '-created_at': '-created_at',
            'created_at': 'created_at',
            'price': 'price',
            '-price': '-price'
        }
        
        if sort_by in valid_sorts:
            queryset = queryset.order_by(valid_sorts[sort_by])
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filter dropdowns data
        context['categories'] = Category.objects.filter(parent__isnull=True)
        context['regions'] = Region.objects.all()
        
        # Pre-select current category and city
        context['selected_category'] = self.category.id if not self.category.is_parent() else None
        context['selected_parent_category'] = self.category.parent.id if self.category.parent else self.category.id
        context['selected_city'] = self.city.id
        context['selected_region'] = self.city.region.id
        
        # Other context data
        context['selected_seller_type'] = self.request.GET.get('seller_type')
        context['selected_sells_to'] = self.request.GET.getlist('sells_to')
        context['seller_type_choices'] = Product.SELLER_TYPE_CHOICES
        context['sells_to_choices'] = Product.SELLS_TO_CHOICES
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_by'] = self.request.GET.get('sort', '-created_at')
        
        # SEO metadata
        context['page_title'] = f"{self.category.name} - {self.city.name}"
        context['page_description'] = f"Обяви за {self.category.name.lower()} в {self.city.name}. Намерете продукти и услуги във вашия град."
        
        return context


class CategoryRegionProductListView(ListView):
    """
    SEO-friendly URL view for combined category + region filters.
    Handles URLs like: /meso/region/sofia-grad/ instead of ?parent_category=123&region=456
    """
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        from django.utils import timezone
        from django.db.models import Q
        from django.db.models.functions import Lower
        from django.http import Http404
        
        # Get category and region from URL slugs
        category_slug = self.kwargs.get('category_slug')
        region_slug = self.kwargs.get('region_slug')
        
        # Look up category by slug
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404(f"Категория '{category_slug}' не съществува")
        
        # Look up region by slug
        try:
            region = Region.objects.get(slug=region_slug)
        except Region.DoesNotExist:
            raise Http404(f"Област '{region_slug}' не съществува")
        
        # Store for use in context
        self.category = category
        self.region = region
        
        # Filter active products within 30 days
        expiry_date = timezone.now() - timezone.timedelta(days=30)
        queryset = Product.objects.filter(is_active=True, created_at__gte=expiry_date)
        
        # Apply category filter (check if parent or subcategory)
        if category.is_parent():
            # Main category - filter by all subcategories
            subcategories = Category.objects.filter(parent=category)
            queryset = queryset.filter(category__in=subcategories)
        else:
            # Subcategory - filter directly
            queryset = queryset.filter(category=category)
        
        # Apply region filter (all cities in region)
        cities = City.objects.filter(region=region)
        queryset = queryset.filter(city__in=cities)
        
        # Search query (optional)
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            search_lower = search_query.lower()
            queryset = queryset.annotate(
                title_lower=Lower('title'),
                description_lower=Lower('description')
            ).filter(
                Q(title_lower__contains=search_lower) | 
                Q(description_lower__contains=search_lower)
            )
        
        # Seller type filter (optional)
        seller_type = self.request.GET.get('seller_type')
        if seller_type:
            queryset = queryset.filter(seller_type=seller_type)
        
        # Sells to filter (optional)
        sells_to = self.request.GET.getlist('sells_to')
        if sells_to:
            from django.db.models import Q
            sells_to_filter = Q()
            for option in sells_to:
                sells_to_filter |= Q(sells_to__contains=[option])
            queryset = queryset.filter(sells_to_filter)
        
        # Sorting
        sort_by = self.request.GET.get('sort', '-created_at')
        valid_sorts = {
            '-created_at': '-created_at',
            'created_at': 'created_at',
            'price': 'price',
            '-price': '-price'
        }
        
        if sort_by in valid_sorts:
            queryset = queryset.order_by(valid_sorts[sort_by])
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filter dropdowns data
        context['categories'] = Category.objects.filter(parent__isnull=True)
        context['regions'] = Region.objects.all()
        
        # Pre-select current category and region
        context['selected_category'] = self.category.id if not self.category.is_parent() else None
        context['selected_parent_category'] = self.category.parent.id if self.category.parent else self.category.id
        context['selected_region'] = self.region.id
        context['selected_city'] = None
        
        # Other context data
        context['selected_seller_type'] = self.request.GET.get('seller_type')
        context['selected_sells_to'] = self.request.GET.getlist('sells_to')
        context['seller_type_choices'] = Product.SELLER_TYPE_CHOICES
        context['sells_to_choices'] = Product.SELLS_TO_CHOICES
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_by'] = self.request.GET.get('sort', '-created_at')
        
        # SEO metadata
        context['page_title'] = f"{self.category.name} - {self.region.name}"
        context['page_description'] = f"Обяви за {self.category.name.lower()} в {self.region.name}. Намерете продукти и услуги в областта."
        
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(pk=self.object.pk)[:4]
        return context


class CategoryDetailView(ListView):
    model = Product
    template_name = 'catalog/category_detail.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        from django.utils import timezone
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        expiry_date = timezone.now() - timezone.timedelta(days=30)
        
        # Ако категорията е родител (има подкатегории), покажи продукти от всички подкатегории
        if self.category.subcategories.exists():
            subcategories = self.category.subcategories.all()
            return Product.objects.filter(
                category__in=subcategories,
                is_active=True,
                created_at__gte=expiry_date
            ).order_by('-created_at')
        else:
            # Ако е подкатегория, покажи директно продуктите от нея
            return Product.objects.filter(
                category=self.category,
                is_active=True,
                created_at__gte=expiry_date
            ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class RegionDetailView(ListView):
    model = Product
    template_name = 'catalog/region_detail.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        from django.utils import timezone
        self.region = get_object_or_404(Region, slug=self.kwargs['slug'])
        expiry_date = timezone.now() - timezone.timedelta(days=30)
        
        # Вземи всички градове в областта
        cities = City.objects.filter(region=self.region)
        return Product.objects.filter(
            city__in=cities,
            is_active=True,
            created_at__gte=expiry_date
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['region'] = self.region
        return context


class CityDetailView(ListView):
    model = Product
    template_name = 'catalog/city_detail.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        from django.utils import timezone
        region = get_object_or_404(Region, slug=self.kwargs['region_slug'])
        self.city = get_object_or_404(City, slug=self.kwargs['slug'], region=region)
        expiry_date = timezone.now() - timezone.timedelta(days=30)
        
        return Product.objects.filter(
            city=self.city,
            is_active=True,
            created_at__gte=expiry_date
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = self.city
        return context


def cities_by_region(request):
    """API endpoint: returns JSON list of cities for a given region id (GET param `region`)."""
    region_id = request.GET.get('region')
    if not region_id:
        return JsonResponse([], safe=False)
    cities = City.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)


def subcategories_by_category(request):
    """API endpoint: returns JSON list of subcategories for a given parent category id (GET param `category`)."""
    category_id = request.GET.get('category')
    if not category_id:
        return JsonResponse([], safe=False)
    subcats = Category.objects.filter(parent_id=category_id).values('id', 'name')
    return JsonResponse(list(subcats), safe=False)


def register(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Деактивиран до имейл потвърждение
            user.save()
            # Генериране на токен за верификация
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # Създаване на линк за активация
            current_site = get_current_site(request)
            activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"
            # Изпращане на имейл
            subject = 'Потвърдете вашата регистрация'
            message = render_to_string('registration/activation_email.txt', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
                'activation_link': activation_link,
            })
            
            import traceback
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True,  # Не вдигай 500 грешка при проблем с пощата
                )
                messages.success(request, 'Регистрацията е успешна! Моля, проверете вашия имейл за потвърждение.')
            except Exception as e:
                user.delete()  # Изтриване на потребителя ако имейлът не се изпрати
                messages.error(request, f'Грешка при изпращане на имейл: {str(e)}')
                return render(request, 'registration/register.html', {'form': form})
            return redirect('catalog:registration_complete')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def activate(request, uidb64, token):
    import traceback
    LOG_PATH = '/home/bghranac/repositories/bghrana/activate_error.log'
    def log_error(msg):
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        log_error(f'Exception in activate-decode: {e}\n{traceback.format_exc()}')
        user = None

    try:
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            # Задай backend, за да избегнеш грешка при multiple authentication backends
            from django.conf import settings
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            login(request, user)
            messages.success(request, 'Акаунтът ви е активиран успешно!')
            return redirect('catalog:product_list')
        else:
            messages.error(request, 'Линкът за активация е невалиден или изтекъл.')
            return redirect('catalog:product_list')
    except Exception as e:
        log_error(f'Exception in activate-final: {e}\n{traceback.format_exc()}')
        messages.error(request, 'Възникна вътрешна грешка при активация. Моля, свържете се с поддръжката.')
        return redirect('catalog:product_list')


def registration_complete(request):
    return render(request, 'registration/registration_complete.html')

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = Region.objects.all()
        context['parent_categories'] = Category.objects.filter(parent__isnull=True)
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        
        # Обработка на 5-те отделни полета за снимки
        for idx in range(1, 6):
            image_file = self.request.FILES.get(f'image{idx}')
            if image_file:
                ProductImage.objects.create(product=self.object, image=image_file, order=idx-1)
        
        return response


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = Region.objects.all()
        context['parent_categories'] = Category.objects.filter(parent__isnull=True)
        
        # Добави текущите снимки за edit режим
        if self.object and self.object.pk:
            images_list = list(self.object.images.order_by('order'))
            context['current_images'] = {
                f'image{i+1}': images_list[i] if i < len(images_list) else None
                for i in range(5)
            }
        
        return context

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Вземи текущите снимки
        existing_images = list(self.object.images.order_by('order'))
        
        # Обработка на новите снимки - добавяме само на празни позиции или заменяме
        for idx in range(1, 6):
            image_file = self.request.FILES.get(f'image{idx}')
            if image_file:
                # Ако има стара снимка на тази позиция, изтрий я
                if idx-1 < len(existing_images):
                    existing_images[idx-1].delete()
                
                # Добави новата снимка
                ProductImage.objects.create(product=self.object, image=image_file, order=idx-1)
        
        return response


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class UserAdsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/user_ads.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)


@login_required
def user_profile(request):
    """Показва профила на потребителя"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    context = {
        'profile': profile,
        'products_count': Product.objects.filter(owner=request.user).count(),
        'active_products_count': Product.objects.filter(owner=request.user, is_active=True).count(),
    }
    return render(request, 'catalog/user_profile.html', context)


@login_required
def edit_profile(request):
    """Редактиране на потребителски профил"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профилът е обновен успешно!')
            return redirect('catalog:user_profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    
    return render(request, 'catalog/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    """Смяна на парола"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Запазване на сесията след смяна на паролата
            messages.success(request, 'Паролата е сменена успешно!')
            return redirect('catalog:user_profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'catalog/change_password.html', {'form': form})


@login_required
def delete_account(request):
    """Изтриване на акаунт"""
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if request.user.check_password(password):
                user = request.user
                auth_logout(request)
                user.delete()
                messages.success(request, 'Акаунтът е изтрит успешно.')
                return redirect('catalog:product_list')
            else:
                messages.error(request, 'Грешна парола!')
    else:
        form = DeleteAccountForm()
    
    return render(request, 'catalog/delete_account.html', {'form': form})


def contact(request):
    """Страница за контакт"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']
            # Изпращане на email
            try:
                send_mail(
                    subject=f'Контактна форма от {email}',
                    message=f'Email: {email}\n\nСъобщение:\n{content}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['support@bghrana.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Вашето съобщение е изпратено успешно!')
                return redirect('catalog:contact')
            except Exception as e:
                messages.error(request, 'Възникна грешка при изпращане на съобщението. Моля, опитайте отново.')
    else:
        form = ContactForm()
    return render(request, 'catalog/contact.html', {'form': form})


def about(request):
    """Страница за нас"""
    return render(request, 'catalog/about.html')


def terms(request):
    """Общи условия"""
    return render(request, 'catalog/terms.html')


def cookie_policy(request):
    """Политика за бисквитки"""
    return render(request, 'catalog/cookie_policy.html')


def seo_page(request, slug):
    """Динамична SEO страница, редактируема от админ панела"""
    page = get_object_or_404(SEOPage, slug=slug, is_active=True)
    return render(request, 'catalog/seo_page.html', {'page': page})
