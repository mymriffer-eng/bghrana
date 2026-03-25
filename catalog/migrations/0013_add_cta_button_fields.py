# Generated manually to add CTA button fields to SEOPage

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_seopage_category_seo_description_category_seo_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seopage',
            name='cta_button_text',
            field=models.CharField(blank=True, help_text='Пример: Виж обяви, Разгледай продукти', max_length=100, verbose_name='Текст на бутона'),
        ),
        migrations.AddField(
            model_name='seopage',
            name='cta_button_url',
            field=models.CharField(blank=True, help_text='Пример: /produkti/?category=med или /produkti/123/', max_length=500, verbose_name='Линк на бутона'),
        ),
        migrations.AddField(
            model_name='seopage',
            name='cta_button_style',
            field=models.CharField(choices=[('success', 'Зелен (Success)'), ('primary', 'Син (Primary)'), ('warning', 'Жълт (Warning)'), ('danger', 'Червен (Danger)'), ('info', 'Светло син (Info)'), ('dark', 'Тъмен (Dark)')], default='success', max_length=20, verbose_name='Стил на бутона'),
        ),
    ]
