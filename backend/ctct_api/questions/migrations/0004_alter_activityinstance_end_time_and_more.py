# Generated by Django 5.0 on 2024-01-23 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_remove_activityparticipation_activity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityinstance',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activityinstance',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]
