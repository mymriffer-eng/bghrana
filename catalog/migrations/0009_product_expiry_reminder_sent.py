# Generated manually for expiry reminder feature

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='expiry_reminder_sent',
            field=models.BooleanField(default=False, verbose_name='Email напомняне изпратено'),
        ),
    ]
