from django.http import HttpResponse
from django.views import View
from .models import Product, Category
from django.urls import reverse


class RobotsTxtView(View):
    """Generate robots.txt for search engine crawlers"""
    def get(self, request):
        lines = [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin/",
            "Disallow: /accounts/",
            "Disallow: /user/",
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
        
        # All products
        for product in Product.objects.filter(is_active=True):
            lines.append('  <url>')
            lines.append(f'    <loc>https://bghrana.com{reverse("product_detail", args=[product.id])}</loc>')
            lines.append(f'    <lastmod>{product.created_at.strftime("%Y-%m-%d")}</lastmod>')
            lines.append('    <changefreq>weekly</changefreq>')
            lines.append('    <priority>0.8</priority>')
            lines.append('  </url>')
        
        # All categories
        for category in Category.objects.all():
            lines.append('  <url>')
            lines.append(f'    <loc>https://bghrana.com/?category={category.id}</loc>')
            lines.append('    <changefreq>daily</changefreq>')
            lines.append('    <priority>0.7</priority>')
            lines.append('  </url>')
        
        lines.append('</urlset>')
        return HttpResponse("\n".join(lines), content_type="application/xml")
