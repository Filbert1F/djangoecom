# Generated by Django 4.2.16 on 2024-10-22 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('IN DELIVERY', 'In delivery'), ('DONE', 'Done')], default='IN DELIVERY', max_length=11),
        ),
    ]
