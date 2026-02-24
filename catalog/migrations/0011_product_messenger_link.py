# Generated manually for messenger_link field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_product_expiry_reminder_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='messenger_link',
            field=models.URLField(blank=True, help_text='Линк към вашия Messenger профил', max_length=300, null=True, verbose_name='Messenger линк'),
        ),
    ]
