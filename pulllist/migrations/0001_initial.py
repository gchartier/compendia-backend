# Generated by Django 2.2.4 on 2019-11-09 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collection', '0008_auto_20191107_1628'),
        ('comic', '0005_comic_is_standard_issue'),
        ('series', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PullList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='collection.Collection')),
            ],
        ),
        migrations.CreateModel(
            name='PullListSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('include_standard_issues', models.BooleanField(default=True)),
                ('include_variants', models.BooleanField(default=False)),
                ('include_TPB', models.BooleanField(default=False)),
                ('include_all_collections', models.BooleanField(default=False)),
                ('include_all', models.BooleanField(default=False)),
                ('pull_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pulllist.PullList')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='series.Series')),
            ],
        ),
        migrations.CreateModel(
            name='PullListComic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comic.Comic')),
                ('pull_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pulllist.PullList')),
            ],
        ),
        migrations.AddField(
            model_name='pulllist',
            name='subscribed_series',
            field=models.ManyToManyField(blank=True, through='pulllist.PullListSeries', to='series.Series'),
        ),
    ]