from django import forms
from .models import Course, Task

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

    
class CourseForm(forms.ModelForm):

    CHOICES = Course.DIFFICULTY_CHOICES

    name = forms.CharField(required=True, label="Название")
    description = forms.CharField(widget=forms.Textarea, required=True, label="Описание")
    difficulty = forms.ChoiceField(label="Сложность", choices=CHOICES)
    is_published = forms.BooleanField(label="Курс опубликован", required=False)

    class Meta:
        model = Course
        fields = ('name', 'description', 'difficulty', 'is_published')


    def clean(self):
        cleaned_data = super(CourseForm, self).clean()

        if 'pk' in self.kw:
            course = get_object_or_404(Course, pk=self.kw['pk'])
            if course.owner != self.request.user:
                self.add_error('name', forms.ValidationError(_("Вы можете редактировать только свои курсы")))


        if not self.request.user.is_teacher:
            self.add_error('name', forms.ValidationError(_("Только преподаватели могут создавать и редактировать курсы")))


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.kw = kwargs.pop('kw', None)
        super(CourseForm, self).__init__(*args, **kwargs)



class TaskForm(forms.ModelForm):

    CHOICES = Task.DIFFICULTY_CHOICES


    name = forms.CharField(required=True, label="Название")
    question = forms.CharField(widget=forms.Textarea, required=True, label="Текст задания")
    answer = forms.CharField(widget=forms.Textarea, required=True, label="Верный ответ")
    keywords = forms.CharField()
    excluded_keywords = forms.CharField()
    difficulty = forms.ChoiceField(label="Сложность", choices=CHOICES)
    is_published = forms.BooleanField(label="Задание опубликовано", required=False)

    class Meta:
        model = Task
        fields = ('name', 'question', 'answer', 'keywords', 'excluded_keywords', 'difficulty', 'is_published')


    def clean(self):
        cleaned_data = super(TaskForm, self).clean()

        course = get_object_or_404(Course, pk=self.kw['course_id'])
        if course.owner != self.request.user:
            self.add_error('name', forms.ValidationError(_("Вы можете создать или отредактировать задание только в своем курсе")))


        if not self.request.user.is_teacher:
            self.add_error('name', forms.ValidationError(_("Только преподаватели могут создавать и редактировать задания")))


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.kw = kwargs.pop('kw', None)
        super(TaskForm, self).__init__(*args, **kwargs)

