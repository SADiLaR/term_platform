import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
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
