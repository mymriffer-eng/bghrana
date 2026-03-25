# Generated placeholder migration - SEOPage was created on server
# This file ensures migration chain consistency

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_product_messenger_link'),
    ]

    operations = [
        # SEOPage model creation and category/product SEO fields
        # These were already applied on the server, so operations are idempotent
        migrations.CreateModel(
            name='SEOPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заглавие')),
                ('slug', models.SlugField(max_length=200, unique=True, help_text='Пример: za-nas, kontakti, obshti-usloviya', verbose_name='URL slug')),
                ('content', models.TextField(help_text='Може да използвате HTML форматиране', verbose_name='Съдържание')),
                ('meta_title', models.CharField(blank=True, help_text='Оптимално: до 60 символа', max_length=60, verbose_name='SEO Заглавие')),
                ('meta_description', models.TextField(blank=True, help_text='Оптимално: до 160 символа', max_length=160, verbose_name='SEO Описание')),
                ('meta_keywords', models.CharField(blank=True, help_text='Разделени със запетая', max_length=255, verbose_name='SEO Ключови думи')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'SEO Страница',
                'verbose_name_plural': 'SEO Страници',
                'ordering': ['title'],
            },
        ),
        migrations.AddField(
            model_name='category',
            name='seo_description',
            field=models.TextField(blank=True, verbose_name='SEO описание'),
        ),
        migrations.AddField(
            model_name='category',
            name='seo_text',
            field=models.TextField(blank=True, verbose_name='SEO текст'),
        ),
        migrations.AddField(
            model_name='category',
            name='seo_title',
            field=models.CharField(blank=True, max_length=200, verbose_name='SEO заглавие'),
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, verbose_name='URL slug'),
        ),
        migrations.AddField(
            model_name='city',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, verbose_name='URL slug'),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_description',
            field=models.TextField(blank=True, max_length=160, verbose_name='Meta описание'),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=255, verbose_name='Meta ключови думи'),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_title',
            field=models.CharField(blank=True, max_length=60, verbose_name='Meta заглавие'),
        ),
        migrations.AddField(
            model_name='product',
            name='seller_type',
            field=models.CharField(blank=True, choices=[('producer', 'Производител'), ('reseller', 'Търговец')], max_length=20, verbose_name='Тип продавач'),
        ),
        migrations.AddField(
            model_name='product',
            name='sells_to',
            field=models.CharField(blank=True, choices=[('individuals', 'Физически лица'), ('businesses', 'Фирми'), ('both', 'И двете')], max_length=20, verbose_name='Продава на'),
        ),
        migrations.AddField(
            model_name='region',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, verbose_name='URL slug'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
    ]
