# Generated by Django 2.0.1 on 2018-02-16 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20180216_1459'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='dbase',
            new_name='task_db',
        ),
        migrations.AddField(
            model_name='task',
            name='task_table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='tasks.Task_table'),
        ),
    ]
