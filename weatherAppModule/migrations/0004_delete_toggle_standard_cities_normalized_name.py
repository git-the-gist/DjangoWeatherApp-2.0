# Generated by Django 5.0.6 on 2024-08-18 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherAppModule', '0003_rename_toggle_toggle_standard'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Toggle_Standard',
        ),
        migrations.AddField(
            model_name='cities',
            name='normalized_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='normalized_name'),
        ),
    ]
