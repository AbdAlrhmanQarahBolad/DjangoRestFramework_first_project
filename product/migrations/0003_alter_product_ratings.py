# Generated by Django 5.0.6 on 2024-08-31 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0002_review"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="ratings",
            field=models.IntegerField(default=0),
        ),
    ]
