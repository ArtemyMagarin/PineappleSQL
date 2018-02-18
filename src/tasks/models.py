from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    EASY = '1'
    SIMPLE = '2'
    MEDIUM = '3'
    HARD = '4'
    VERY_HARD = '5'
    DIFFICULTY_CHOICES = (
        (EASY, 'Легко'),
        (SIMPLE, 'Просто'),
        (MEDIUM, 'Средне'),
        (HARD, 'Сложно'),
        (VERY_HARD, 'Очень сложно')
    )

    difficulty = models.CharField(
        max_length=1,
        choices=DIFFICULTY_CHOICES,
        default=EASY
    )

    owner = models.ForeignKey(
        'accounts.User', 
        related_name='courses',
        null=False, blank=False,
        on_delete=models.PROTECT
    )

    is_published = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    published_date = models.DateTimeField(null=True)

    def get_absolute_url(self):
        return reverse_lazy("tasks:view_course", kwargs={'pk': self.id})



class Task_db(models.Model):
    owner = models.ForeignKey(
        'accounts.User', 
        related_name="task_dbs", 
        on_delete=models.CASCADE,
    )
    dbname = models.CharField(max_length=150)
    staffname = models.CharField(max_length=255, null=True)

    description = models.TextField(null=True)

    def __str__(self):
        return self.dbname

    def get_absolute_url(self):
        return reverse_lazy("tasks:view_task_db", kwargs={'pk': self.id})


class Task_table(models.Model):
    owner = models.ForeignKey(
        'accounts.User', 
        related_name="task_tables", 
        on_delete=models.CASCADE,
    )
    db = models.ForeignKey(
        Task_db,
        related_name="task_tables",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=150)
    staffname = models.CharField(max_length=255, null=True)

    description = models.TextField(default="--")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("tasks:view_task_table", kwargs={'pk': self.id})



class Task(models.Model):
    owner = models.ForeignKey(
        'accounts.User', 
        related_name='tasks',
        null=False, blank=False,
        on_delete=models.PROTECT
    )

    name = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()
    keywords = models.CharField(max_length=255)
    excluded_keywords = models.CharField(max_length=255)

    task_db = models.ForeignKey(
        Task_db, 
        related_name='tasks', 
        null=True,
        on_delete=models.PROTECT
    )

    task_table = models.ForeignKey(
        Task_table, 
        related_name='tasks', 
        null=True,
        on_delete=models.PROTECT
    )


    is_published = models.BooleanField(default=False)

    course = models.ForeignKey(
        Course, 
        related_name='tasks',
        null=False, blank=False,
        on_delete=models.PROTECT
    )

    EASY = '1'
    SIMPLE = '2'
    MEDIUM = '3'
    HARD = '4'
    VERY_HARD = '5'
    DIFFICULTY_CHOICES = (
        (EASY, 'Легко'),
        (SIMPLE, 'Просто'),
        (MEDIUM, 'Средне'),
        (HARD, 'Сложно'),
        (VERY_HARD, 'Очень сложно')
    )

    difficulty = models.CharField(
        max_length=1,
        choices=DIFFICULTY_CHOICES,
        default=EASY
    )

    def get_absolute_url(self):
        return reverse_lazy("tasks:view_task", kwargs={'pk': self.id})


class Like(models.Model):
    owner = models.ForeignKey(
        'accounts.User', 
        related_name="+", 
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course, 
        related_name="likes", 
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (("owner", "course"),)


class Progress(models.Model):
    owner = models.ForeignKey(
        'accounts.User', 
        related_name="progress", 
        on_delete=models.CASCADE,
    )

    course = models.ForeignKey(
        Course, 
        related_name="progress", 
        on_delete=models.CASCADE,
    )

    task = models.ForeignKey(
        Task,
        related_name="progress",
        on_delete=models.CASCADE,
        null=True
    )

    data = models.TextField(null=True, blank=True)

    is_passed = models.BooleanField(default=False)

    class Meta:
        unique_together = (("owner", "course", "task"),)


class Subscribes(models.Model):
    owner = models.ForeignKey(
        'accounts.User', 
        related_name="subscribes", 
        on_delete=models.CASCADE,
    )

    course = models.ForeignKey(
        Course, 
        related_name="subscribes", 
        on_delete=models.CASCADE,
    )

    is_passed = models.BooleanField(default=False)
