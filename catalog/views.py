from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout as auth_logout, update_session_auth_hash
from .models import Product, Category, Region, City, ProductImage, UserProfile
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

@csrf_exempt
@require_http_methods(["GET", "POST"])
def logout(request):
    auth_logout(request)
    return redirect('catalog:product_list')

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

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
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_by'] = self.request.GET.get('sort', '-created_at')
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
                print('REGISTER ERROR:', str(e))
                traceback.print_exc()
                user.delete()  # Изтриване на потребителя ако имейлът не се изпрати
                messages.error(request, f'Грешка при изпращане на имейл: {str(e)}')
                return render(request, 'registration/register.html', {'form': form})
            
            return redirect('catalog:registration_complete')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Акаунтът ви е активиран успешно!')
        return redirect('catalog:product_list')
    else:
        messages.error(request, 'Линкът за активация е невалиден или изтекъл.')
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
        
        # Проверка дали има нови снимки
        has_new_images = any(self.request.FILES.get(f'image{i}') for i in range(1, 6))
        
        if has_new_images:
            # Изтрий старите снимки
            self.object.images.all().delete()
            
            # Добави новите снимки
            for idx in range(1, 6):
                image_file = self.request.FILES.get(f'image{idx}')
                if image_file:
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
                    recipient_list=['galinpavloveto@gmail.com'],
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
