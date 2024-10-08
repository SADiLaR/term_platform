# Generated by Django 5.0.2 on 2024-05-27 10:56

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0006_documentfile_document_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentfile',
            options={'verbose_name': 'Document File', 'verbose_name_plural': 'Document Files'},
        ),
        migrations.AlterModelOptions(
            name='historicaldocumentfile',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Document File', 'verbose_name_plural': 'historical Document Files'},
        ),
        migrations.AlterModelOptions(
            name='historicalinstitution',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Institution', 'verbose_name_plural': 'historical Institutions'},
        ),
        migrations.AlterModelOptions(
            name='historicallanguage',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Language', 'verbose_name_plural': 'historical Languages'},
        ),
        migrations.AlterModelOptions(
            name='historicalproject',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Project', 'verbose_name_plural': 'historical Projects'},
        ),
        migrations.AlterModelOptions(
            name='historicalsubject',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Subject', 'verbose_name_plural': 'historical Subjects'},
        ),
        migrations.AlterModelOptions(
            name='institution',
            options={'verbose_name': 'Institution', 'verbose_name_plural': 'Institutions'},
        ),
        migrations.AlterModelOptions(
            name='language',
            options={'verbose_name': 'Language', 'verbose_name_plural': 'Languages'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'verbose_name': 'Subject', 'verbose_name_plural': 'Subjects'},
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='available',
            field=models.BooleanField(default=True, verbose_name='available'),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='document_data',
            field=models.TextField(blank=True, verbose_name='document data'),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='document_type',
            field=models.CharField(choices=[('Glossary', 'Glossary'), ('Policy', 'Policy')], max_length=200, verbose_name='document type'),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.institution', verbose_name='institution'),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='languages',
            field=models.ManyToManyField(blank=True, to='general.language', verbose_name='languages'),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='license',
            field=models.CharField(choices=[('(c)', 'All rights reserved'), ('CC0', 'No rights reserved'), ('CC BY', 'Creative Commons Attribution'), ('CC BY-SA', 'Creative Commons Attribution-ShareAlike'), ('CC BY-NC', 'Creative Commons Attribution-NonCommercial'), ('CC BY-NC-SA', 'Creative Commons Attribution-NonCommercial-ShareAlike')], default='(c)', help_text='<a\n              href="https://creativecommons.org/share-your-work/cclicenses/"\n              rel="noreferrer"\n              target="_blank"\n          >\n          More information about Creative Commons licenses.\n        </a>', max_length=200, verbose_name='license'),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='mime_type',
            field=models.CharField(blank=True, help_text='This input will auto-populate.', max_length=200, verbose_name='MIME type'),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='general.subject', verbose_name='subjects'),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='title',
            field=models.CharField(max_length=200, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='uploaded_file',
            field=models.FileField(blank=True, help_text='PDF files up to 10MB are allowed.', upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='historicaldocumentfile',
            name='available',
            field=models.BooleanField(default=True, verbose_name='available'),
        ),
        migrations.AlterField(
            model_name='historicaldocumentfile',
            name='document_type',
            field=models.CharField(choices=[('Glossary', 'Glossary'), ('Policy', 'Policy')], max_length=200, verbose_name='document type'),
        ),
        migrations.AlterField(
            model_name='historicaldocumentfile',
            name='institution',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='general.institution', verbose_name='institution'),
        ),
        migrations.AlterField(
            model_name='historicaldocumentfile',
            name='license',
            field=models.CharField(choices=[('(c)', 'All rights reserved'), ('CC0', 'No rights reserved'), ('CC BY', 'Creative Commons Attribution'), ('CC BY-SA', 'Creative Commons Attribution-ShareAlike'), ('CC BY-NC', 'Creative Commons Attribution-NonCommercial'), ('CC BY-NC-SA', 'Creative Commons Attribution-NonCommercial-ShareAlike')], default='(c)', help_text='<a\n              href="https://creativecommons.org/share-your-work/cclicenses/"\n              rel="noreferrer"\n              target="_blank"\n          >\n          More information about Creative Commons licenses.\n        </a>', max_length=200, verbose_name='license'),
        ),
        migrations.AlterField(
            model_name='historicaldocumentfile',
            name='mime_type',
            field=models.CharField(blank=True, help_text='This input will auto-populate.', max_length=200, verbose_name='MIME type'),
        ),
        migrations.AlterField(
            model_name='historicaldocumentfile',
            name='title',
            field=models.CharField(max_length=200, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='historicaldocumentfile',
            name='uploaded_file',
            field=models.TextField(blank=True, help_text='PDF files up to 10MB are allowed.', max_length=100, validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='uploaded file'),
        ),
        migrations.AlterField(
            model_name='historicalinstitution',
            name='abbreviation',
            field=models.CharField(max_length=200, verbose_name='abbreviation'),
        ),
        migrations.AlterField(
            model_name='historicalinstitution',
            name='email',
            field=models.EmailField(blank=True, max_length=200, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='historicalinstitution',
            name='logo',
            field=models.TextField(blank=True, max_length=100, verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='historicalinstitution',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='historicallanguage',
            name='name',
            field=models.CharField(db_index=True, max_length=150, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='historicalproject',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='end date'),
        ),
        migrations.AlterField(
            model_name='historicalproject',
            name='logo',
            field=models.TextField(blank=True, max_length=100, verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='historicalproject',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='historicalproject',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='start date'),
        ),
        migrations.AlterField(
            model_name='historicalsubject',
            name='name',
            field=models.CharField(db_index=True, max_length=150, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='abbreviation',
            field=models.CharField(max_length=200, verbose_name='abbreviation'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='email',
            field=models.EmailField(blank=True, max_length=200, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='logo',
            field=models.ImageField(blank=True, upload_to='institutions/logos/', verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='end date'),
        ),
        migrations.AlterField(
            model_name='project',
            name='languages',
            field=models.ManyToManyField(blank=True, to='general.language', verbose_name='languages'),
        ),
        migrations.AlterField(
            model_name='project',
            name='logo',
            field=models.ImageField(blank=True, upload_to='projects/logos/', verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='start date'),
        ),
        migrations.AlterField(
            model_name='project',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='general.subject', verbose_name='subjects'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='name'),
        ),
    ]
