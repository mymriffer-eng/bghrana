from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
from .views_seo import RobotsTxtView, SitemapXMLView

app_name = 'catalog'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('category-redirect/', views.category_redirect, name='category_redirect'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('api/cities/', views.cities_by_region, name='api_cities'),
    path('api/subcategories/', views.subcategories_by_category, name='api_subcategories'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('registration-complete/', views.registration_complete, name='registration_complete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.logout, name='logout'),
    path('ads/new/', views.ProductCreateView.as_view(), name='product_create'),
    path('ads/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('ads/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('my-ads/', views.UserAdsListView.as_view(), name='user_ads'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/delete-account/', views.delete_account, name='delete_account'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('cookies/', views.cookie_policy, name='cookie_policy'),
    
    # SEO
    path('robots.txt', RobotsTxtView.as_view(), name='robots_txt'),
    path('sitemap.xml', SitemapXMLView.as_view(), name='sitemap_xml'),
    
    # Dynamic SEO Pages (трябва да е накрая за да не пречи на другите URL-и)
    path('<slug:slug>/', views.seo_page, name='seo_page'),
]
