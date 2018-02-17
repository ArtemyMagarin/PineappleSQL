from django import forms
from .models import Course, Task, Task_db, Task_table

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

    
class CourseForm(forms.ModelForm):

    CHOICES = Course.DIFFICULTY_CHOICES

    name = forms.CharField(required=True, label="Название")
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Напишите развернутое описание всего курса'}), required=True, label="Описание")
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
    task_db = forms.ModelChoiceField(queryset=Task_db.objects.all(), empty_label="-----", required=True, label="База данных")
    task_table = forms.ModelChoiceField(queryset=Task_table.objects.all(), empty_label="-----", required=True, label="Таблица")
    question = forms.CharField(widget=forms.Textarea, required=True, label="Текст задания")
    answer = forms.CharField(widget=forms.Textarea, required=True, label="Эталонный ответ")
    keywords = forms.CharField(label="Ключевые слова", help_text="Слова, которые обязаны быть в запросе студента")
    excluded_keywords = forms.CharField(label="Исключенные слова", help_text="Слова, которых в запросе студента быть не должно")
    difficulty = forms.ChoiceField(label="Сложность", choices=CHOICES)
    is_published = forms.BooleanField(label="Задание опубликовано", required=False)

    class Meta:
        model = Task
        fields = ('name', 'task_db', 'task_table', 'question', 'answer', 'keywords', 'excluded_keywords', 'difficulty', 'is_published')


    def clean(self):
        cleaned_data = super(TaskForm, self).clean()

        course = get_object_or_404(Course, pk=self.kw['course_id'])
        if course.owner != self.request.user:
            self.add_error('name', forms.ValidationError(_("Вы можете создать или отредактировать задание только в своем курсе")))


        if not self.request.user.is_teacher:
            self.add_error('name', forms.ValidationError(_("Только преподаватели могут создавать и редактировать задания")))


        if cleaned_data['task_db'] and cleaned_data['task_table']:
            db = cleaned_data['task_db']
            tbl = cleaned_data['task_table']

            if not db or db.owner != self.request.user:
                self.add_error('task_db', forms.ValidationError(_("Базы данных не существует или она принадлежит не вам")))

            if not tbl or tbl.owner != self.request.user:
                self.add_error('task_table', forms.ValidationError(_("Таблицы не существует или она принадлежит не вам")))

            if tbl.db != db:
                self.add_error('task_table', forms.ValidationError(_("Таблица принадлежит другой базе данных (%(db))"), params={'db': tbl.db}))


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.kw = kwargs.pop('kw', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['task_db'].queryset = Task_db.objects.filter(owner=self.request.user)
        self.fields['task_table'].queryset = Task_table.objects.filter(owner=self.request.user)



class DataBaseForm(forms.ModelForm):
    dbname = forms.CharField(required=True, label="Название")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Описание")


    class Meta:
        model = Task_db
        fields = ['dbname', 'description']

    def clean(self):
        cleaned_data = super(DataBaseForm, self).clean()

        if not self.request.user.is_teacher:
            self.add_error('dbname', forms.ValidationError(_("Только преподаватели могут создавать базы данных")))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.kw = kwargs.pop('kw', None)
        super(DataBaseForm, self).__init__(*args, **kwargs)



class TableForm(forms.ModelForm):
    db = forms.ModelChoiceField(queryset=Task_db.objects.all(), empty_label="-----", required=True, label="База данных")
    name = forms.CharField(required=True, label="Название")
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Описание структуры таблицы'}), required=False, label="Описание")
    create_query = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Введите запрос для создания таблицы'}), required=True, label="Запрос для создания таблицы")
    data_query = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Введите запрос для добавления данных в таблицу. (INSERT INTO tbl_name [(col_name [, col_name] ...)] VALUES (value_list) [, (value_list)] ...)'}), required=True, label="Запрос для добавления данных")


    class Meta:
        model = Task_table
        fields = ['db', 'name', 'description']

    def clean(self):
        cleaned_data = super(TableForm, self).clean()

        if not self.request.user.is_teacher:
            self.add_error('dbname', forms.ValidationError(_("Только преподаватели могут создавать базы данных")))

        db = cleaned_data['db']
        if not db or db.owner != self.request.user:
            self.add_error('db', forms.ValidationError(_("Базы данных не существует или она принадлежит не вам")))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.kw = kwargs.pop('kw', None)
        super(TableForm, self).__init__(*args, **kwargs)
        self.fields['db'].queryset = Task_db.objects.filter(owner=self.request.user)
