# Generated by Django 2.1rc1 on 2018-07-23 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0007_stdsubject_subject_total_marks'),
    ]

    operations = [
        migrations.AddField(
            model_name='marks',
            name='subject_total_marks',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Total Marks'),
        ),
    ]