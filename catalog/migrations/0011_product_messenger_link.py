# Generated manually for messenger_link field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_seopage_category_seo_description_category_seo_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='messenger_link',
            field=models.URLField(blank=True, help_text='Линк към вашия Messenger профил', max_length=300, null=True, verbose_name='Messenger линк'),
        ),
    ]
