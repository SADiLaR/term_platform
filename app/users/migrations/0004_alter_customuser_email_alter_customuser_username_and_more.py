# Generated by Django 5.0.6 on 2024-07-19 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_historicalcustomuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(unique=True),
        ),
        migrations.AlterField(
            model_name='historicalcustomuser',
            name='email',
            field=models.EmailField(db_index=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='historicalcustomuser',
            name='username',
            field=models.CharField(db_index=True),
        ),
    ]