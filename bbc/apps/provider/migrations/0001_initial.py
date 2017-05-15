# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('npi', models.CharField(default='', max_length=10, blank=True)),
                ('fhir_json_snipit', models.TextField(default='', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Affiliation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('npi', models.CharField(default='', max_length=10, blank=True)),
                ('fhir_json_snipit', models.TextField(default='', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('npi', models.CharField(default='', max_length=10, blank=True)),
                ('fhir_json_snipit', models.TextField(default='', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('npi', models.CharField(default='', max_length=10)),
                ('fhir_id', models.CharField(default='', max_length=24)),
                ('organization_name', models.CharField(default='', max_length=256)),
                ('doing_business_as', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Practitioner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('npi', models.CharField(default='', unique=True, max_length=10)),
                ('fhir_id', models.CharField(default='', unique=True, max_length=24, verbose_name='FHIR ID')),
                ('first_name', models.CharField(default='', max_length=256, blank=True)),
                ('last_name', models.CharField(default='', max_length=256, blank=True)),
                ('doing_business_as', models.CharField(default='', max_length=256, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Taxonomy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('npi', models.CharField(default='', max_length=10, blank=True)),
                ('fhir_json_snipit', models.TextField(default='', max_length=2000)),
            ],
        ),
    ]
