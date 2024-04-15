import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('abbreviation', models.CharField(max_length=200)),
                ('url', models.URLField(blank=True)),
                ('email', models.EmailField(blank=True, max_length=200)),
                ('logo', models.FileField(blank=True, upload_to='logos/')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('iso_code', models.CharField(help_text='Enter the ISO code for the language', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('logo', models.FileField(blank=True, upload_to='logos/')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('institution', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='general.institution', verbose_name='institution')),
                ('languages', models.ManyToManyField(blank=True, to='general.language')),
                ('subjects', models.ManyToManyField(blank=True, to='general.subject')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField(blank=True)),
                ('uploaded_file', models.FileField(blank=True, help_text='Only PDF files are allowed.', upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('available', models.BooleanField(default=True)),
                ('license', models.CharField(choices=[('MIT', 'MIT'), ('GNU', 'GNU'), ('Apache', 'Apache')], max_length=200)),
                ('mime_type', models.CharField(blank=True, help_text='This input will auto-populate.', max_length=200)),
                ('document_type', models.CharField(choices=[('Glossary', 'Glossary'), ('Translation', 'Translation')], max_length=200)),
                ('Institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.institution')),
                ('languages', models.ManyToManyField(blank=True, to='general.language')),
                ('subjects', models.ManyToManyField(blank=True, to='general.subject')),
            ],
        ),
    ]
