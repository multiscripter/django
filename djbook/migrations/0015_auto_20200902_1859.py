# Generated by Django 3.1 on 2020-09-02 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djbook', '0014_auto_20200902_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rus',
            name='word',
            field=models.CharField(max_length=32, unique=True, verbose_name='Слово'),
        ),
    ]
