# Generated by Django 5.0.2 on 2024-02-23 11:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContributingCentre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('url', models.URLField()),
                ('logo', models.FileField(blank=True, upload_to='logos/')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('iso_code', models.CharField(help_text='Enter the ISO code for the language', max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('abbreviation', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('email', models.EmailField(max_length=200)),
                ('logo', models.FileField(blank=True, upload_to='logos/')),
                ('contributing_centre', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='general.contributingcentre')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('contributing_centre', models.ManyToManyField(blank=True, related_name='subjects', to='general.contributingcentre')),
            ],
        ),
    ]
