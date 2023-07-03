# Generated by Django 4.2.2 on 2023-07-03 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_productmodel_user'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='productmodel',
            index=models.Index(fields=['category'], name='products_categor_fce6e6_idx'),
        ),
        migrations.AddIndex(
            model_name='productmodel',
            index=models.Index(fields=['name'], name='products_name_6f9890_idx'),
        ),
    ]
