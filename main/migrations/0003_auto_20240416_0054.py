# Generated by Django 3.2.25 on 2024-04-16 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20240416_0037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='menu_name',
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='url',
            field=models.CharField(default='', max_length=200),
        ),
    ]
