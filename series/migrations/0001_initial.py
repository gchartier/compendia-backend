# Generated by Django 2.2.4 on 2019-10-13 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('publisher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('alt_id', models.CharField(blank=True, max_length=100, null=True)),
                ('genre', models.CharField(blank=True, max_length=50, null=True)),
                ('years', models.CharField(blank=True, max_length=100, null=True)),
                ('is_one_shot', models.BooleanField(default=False)),
                ('is_mini_series', models.BooleanField(default=False)),
                ('mini_series_limit', models.PositiveSmallIntegerField(null=True)),
                ('imprint', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='publisher.Imprint')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publisher.Publisher')),
            ],
        ),
    ]
