# Generated by Django 5.0.3 on 2024-05-04 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0003_alter_featurespurchaseordermodel_issue_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featureshistoricalperformancemodel',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
