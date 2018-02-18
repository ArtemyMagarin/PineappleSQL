# Generated by Django 2.0.1 on 2018-02-10 20:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('difficulty', models.CharField(choices=[('1', 'Легко'), ('2', 'Просто'), ('3', 'Средне'), ('4', 'Сложно'), ('5', 'Очень сложно')], default='1', max_length=1)),
                ('is_published', models.BooleanField(default=False)),
                ('rating', models.IntegerField(default=0)),
                ('published_date', models.DateTimeField(null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='courses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='tasks.Course')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(blank=True, null=True)),
                ('is_passed', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='tasks.Course')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('keywords', models.CharField(max_length=255)),
                ('excluded_keywords', models.CharField(max_length=255)),
                ('is_published', models.BooleanField(default=False)),
                ('difficulty', models.CharField(choices=[('1', 'Легко'), ('2', 'Просто'), ('3', 'Средне'), ('4', 'Сложно'), ('5', 'Очень сложно')], default='1', max_length=1)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='tasks.Course')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='progress',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='tasks.Task'),
        ),
        migrations.AlterUniqueTogether(
            name='progress',
            unique_together={('owner', 'course', 'task')},
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('owner', 'course')},
        ),
    ]
