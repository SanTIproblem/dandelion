# Generated by Django 4.0 on 2022-03-29 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='normaluser',
            name='clean_password',
            field=models.CharField(blank=True, max_length=128, verbose_name='密码'),
        ),
    ]