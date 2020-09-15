# Generated by Django 2.2.4 on 2019-10-28 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comic', '0004_comic_imprint'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ComicBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.Collection')),
                ('comics', models.ManyToManyField(blank=True, to='comic.Comic')),
            ],
        ),
        migrations.CreateModel(
            name='CollectedComic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_collected', models.DateTimeField(blank=True)),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bought_at', models.CharField(blank=True, max_length=50)),
                ('condition', models.CharField(blank=True, max_length=50)),
                ('grade', models.DecimalField(blank=True, decimal_places=1, max_digits=2)),
                ('quantity', models.PositiveSmallIntegerField(blank=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.Collection')),
                ('comic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comic.Comic')),
            ],
        ),
    ]