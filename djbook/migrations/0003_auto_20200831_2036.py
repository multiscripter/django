# Generated by Django 3.1 on 2020-08-31 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djbook', '0002_auto_20200831_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxonomy',
            name='parent',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, parent_link=True, to='djbook.taxonomy'),
        ),
    ]
