# Generated by Django 2.2.4 on 2019-10-21 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0001_initial'),
        ('comic', '0003_comic'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='imprint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='publisher.Imprint'),
        ),
    ]