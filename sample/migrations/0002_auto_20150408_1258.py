# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='samplecount',
            name='num',
        ),
        migrations.AddField(
            model_name='samplecount',
            name='text',
            field=models.CharField(default='first', max_length=500),
            preserve_default=False,
        ),
    ]
