# Generated by Django 2.0.1 on 2018-02-16 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_task_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='task_db',
            name='staffname',
            field=models.TextField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='task_table',
            name='staffname',
            field=models.TextField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='task_db',
            name='dbname',
            field=models.TextField(max_length=150),
        ),
        migrations.AlterField(
            model_name='task_table',
            name='name',
            field=models.TextField(max_length=150),
        ),
    ]
