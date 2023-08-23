# Generated by Django 4.2.2 on 2023-08-17 13:55

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('api_order', '0003_alter_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_order_cost',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
    ]
