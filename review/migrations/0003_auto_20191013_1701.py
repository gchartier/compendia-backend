# Generated by Django 2.2.4 on 2019-10-13 21:01

from django.db import migrations, models
import review.models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20191013_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(null=True, validators=[review.models.validate_rating]),
        ),
    ]