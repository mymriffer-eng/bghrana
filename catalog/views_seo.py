from django.http import HttpResponse
from django.views import View
from .models import Product, Category, Region, City, SEOPage
from django.urls import reverse
from django.utils import timezone


class RobotsTxtView(View):
    """Generate robots.txt for search engine crawlers"""
    def get(self, request):
        lines = [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin/",
            "Disallow: /accounts/",
            "Disallow: /user/",
            "Disallow: /*?page=",
            "Disallow: /*?parent_category=",
            "Disallow: /*?category=",
            "Disallow: /*?region=",
            "Disallow: /*?city=",
            "Crawl-delay: 1",
            "",
            f"Sitemap: https://bghrana.com/sitemap.xml",
        ]
        return HttpResponse("\n".join(lines), content_type="text/plain")


class SitemapXMLView(View):
    """Generate sitemap.xml for search engines"""
    def get(self, request):
        from datetime import datetime
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ]
        
        # Homepage
        lines.append('  <url>')
        lines.append('    <loc>https://bghrana.com/</loc>')
        lines.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
        lines.append('    <changefreq>daily</changefreq>')
        lines.append('    <priority>1.0</priority>')
        lines.append('  </url>')
        
        # Categories (само категории с продукти и slug)
        categories = Category.objects.filter(
            products__isnull=False,
            slug__isnull=False
        ).exclude(slug='').distinct()
        
        for category in categories:
            lines.append('  <url>')
            lines.append(f'    <loc>https://bghrana.com/category/{category.slug}/</loc>')
            # Вземи най-новия продукт от категорията за lastmod
            latest_product = category.products.filter(is_active=True).order_by('-updated_at').first()
            if latest_product:
                lines.append(f'    <lastmod>{latest_product.updated_at.strftime("%Y-%m-%d")}</lastmod>')
            lines.append('    <changefreq>daily</changefreq>')
            lines.append('    <priority>0.8</priority>')
            lines.append('  </url>')
        
        # Regions (само области с продукти и slug)
        regions = Region.objects.filter(slug__isnull=False).exclude(slug='')
        
        for region in regions:
            # Проверка дали има продукти в областта
            cities = City.objects.filter(region=region)
            expiry_date = timezone.now() - timezone.timedelta(days=180)
            has_products = Product.objects.filter(
                city__in=cities, 
                is_active=True, 
                created_at__gte=expiry_date
            ).exists()
            
            if has_products:
                lines.append('  <url>')
                lines.append(f'    <loc>https://bghrana.com/region/{region.slug}/</loc>')
                latest_product = Product.objects.filter(
                    city__in=cities, 
                    is_active=True
                ).order_by('-updated_at').first()
                if latest_product:
                    lines.append(f'    <lastmod>{latest_product.updated_at.strftime("%Y-%m-%d")}</lastmod>')
                lines.append('    <changefreq>daily</changefreq>')
                lines.append('    <priority>0.7</priority>')
                lines.append('  </url>')
        
        # Cities (само градове с продукти и slug)
        cities = City.objects.filter(slug__isnull=False, region__slug__isnull=False).exclude(slug='')
        
        for city in cities:
            expiry_date = timezone.now() - timezone.timedelta(days=180)
            has_products = Product.objects.filter(
                city=city, 
                is_active=True, 
                created_at__gte=expiry_date
            ).exists()
            
            if has_products:
                lines.append('  <url>')
                lines.append(f'    <loc>https://bghrana.com/region/{city.region.slug}/{city.slug}/</loc>')
                latest_product = Product.objects.filter(
                    city=city, 
                    is_active=True
                ).order_by('-updated_at').first()
                if latest_product:
                    lines.append(f'    <lastmod>{latest_product.updated_at.strftime("%Y-%m-%d")}</lastmod>')
                lines.append('    <changefreq>weekly</changefreq>')
                lines.append('    <priority>0.6</priority>')
                lines.append('  </url>')
        
        # Active products (последните 30 дни)
        expiry_date = timezone.now() - timezone.timedelta(days=180)
        products = Product.objects.filter(is_active=True, created_at__gte=expiry_date).order_by('-created_at')
        
        for product in products:
            lines.append('  <url>')
            lines.append(f'    <loc>https://bghrana.com{reverse("catalog:product_detail", args=[product.id])}</loc>')
            lines.append(f'    <lastmod>{product.updated_at.strftime("%Y-%m-%d")}</lastmod>')
            lines.append('    <changefreq>weekly</changefreq>')
            lines.append('    <priority>0.5</priority>')
            lines.append('  </url>')
        
        # SEO Pages
        seo_pages = SEOPage.objects.filter(is_active=True)
        for page in seo_pages:
            lines.append('  <url>')
            lines.append(f'    <loc>https://bghrana.com/{page.slug}/</loc>')
            lines.append(f'    <lastmod>{page.updated_at.strftime("%Y-%m-%d")}</lastmod>')
            lines.append('    <changefreq>monthly</changefreq>')
            lines.append('    <priority>0.6</priority>')
            lines.append('  </url>')
        
        # About page (статична)
        lines.append('  <url>')
        lines.append('    <loc>https://bghrana.com/about/</loc>')
        lines.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
        lines.append('    <changefreq>monthly</changefreq>')
        lines.append('    <priority>0.4</priority>')
        lines.append('  </url>')
        
        lines.append('</urlset>')
        return HttpResponse("\n".join(lines), content_type="text/xml; charset=utf-8")
