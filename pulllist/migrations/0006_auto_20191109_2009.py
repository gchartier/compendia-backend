# Generated by Django 2.2.4 on 2019-11-10 01:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pulllist', '0005_auto_20191109_1927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pulllist',
            name='comics',
        ),
        migrations.DeleteModel(
            name='PullListComic',
        ),
    ]
