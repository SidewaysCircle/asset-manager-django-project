# Generated by Django 4.0.3 on 2022-04-05 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_alter_laptop_laptopuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptop',
            name='laptopUser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='assets.client'),
        ),
    ]