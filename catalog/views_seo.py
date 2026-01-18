from django.http import HttpResponse
from django.views import View
from .models import Product, Category
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
            "Crawl-delay: 1",
            "",
            f"Sitemap: https://bghrana.com/sitemap.xml",
        ]
        return HttpResponse("\n".join(lines), content_type="text/plain")


class SitemapXMLView(View):
    """Generate sitemap.xml for search engines"""
    def get(self, request):
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ]
        
        # Homepage
        lines.append('  <url>')
        lines.append('    <loc>https://bghrana.com/</loc>')
        lines.append('    <changefreq>daily</changefreq>')
        lines.append('    <priority>1.0</priority>')
        lines.append('  </url>')
        
        # About page
        lines.append('  <url>')
        lines.append('    <loc>https://bghrana.com/about/</loc>')
        lines.append('    <changefreq>monthly</changefreq>')
        lines.append('    <priority>0.5</priority>')
        lines.append('  </url>')
        
        # Active products (последните 30 дни)
        expiry_date = timezone.now() - timezone.timedelta(days=30)
        products = Product.objects.filter(is_active=True, created_at__gte=expiry_date).order_by('-created_at')
        
        for product in products:
            lines.append('  <url>')
            lines.append(f'    <loc>https://bghrana.com{reverse("catalog:product_detail", args=[product.id])}</loc>')
            lines.append(f'    <lastmod>{product.updated_at.strftime("%Y-%m-%d")}</lastmod>')
            lines.append('    <changefreq>weekly</changefreq>')
            lines.append('    <priority>0.8</priority>')
            lines.append('  </url>')
        
        # Categories (само подкатегории с продукти)
        for category in Category.objects.filter(products__isnull=False).distinct():
            lines.append('  <url>')
            lines.append(f'    <loc>https://bghrana.com/?category={category.id}</loc>')
            lines.append('    <changefreq>daily</changefreq>')
            lines.append('    <priority>0.7</priority>')
            lines.append('  </url>')
        
        lines.append('</urlset>')
        return HttpResponse("\n".join(lines), content_type="application/xml")
