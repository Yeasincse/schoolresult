# Generated by Django 2.0.6 on 2018-07-11 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0003_auto_20180711_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfo',
            name='std_gpa',
            field=models.CharField(blank=True, default='F', max_length=10, null=True, verbose_name='GPA'),
        ),
    ]