# Generated by Django 4.2.7 on 2024-05-02 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharma', '0012_delete_customer_delete_purchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='delivery_status',
            field=models.CharField(default='received', max_length=255),
        ),
    ]