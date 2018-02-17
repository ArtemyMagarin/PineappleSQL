from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse


from .forms import CourseForm, TaskForm, DataBaseForm, TableForm
from .models import Course, Task, Progress, Subscribes, Task_db, Task_table

from django.shortcuts import redirect, get_object_or_404


from dbmanager.manager import DBManager


class CourseCreate(CreateView):
    template_name = 'tasks/course_form.html'
    form_class = CourseForm
    model = Course

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            return redirect('tasks:course_list')
        return super(CourseCreate, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.owner = self.request.user
        if 'is_published' in form.cleaned_data and form.cleaned_data['is_published'] == 'on':
            form.instance.published_date = timezone.now()
        form.save() 

        return super(CourseCreate, self).form_valid(form)

    def get_form_kwargs(self):
        kw = super(CourseCreate, self).get_form_kwargs()
        kw['request'] = self.request
        kw['kw'] = self.kwargs
        return kw


class CourseUpdate(UpdateView):
    template_name = 'tasks/course_form.html'
    form_class = CourseForm
    model = Course

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            return redirect('tasks:view_course', pk=kwargs['pk'])
        return super(CourseUpdate, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        if 'is_published' in form.cleaned_data and form.cleaned_data['is_published'] == 'on':
            form.instance.published_date = timezone.now()
        form.save() 
        return super(CourseUpdate, self).form_valid(form)

    def get_form_kwargs(self):
        kw = super(CourseUpdate, self).get_form_kwargs()
        kw['request'] = self.request
        kw['kw'] = self.kwargs
        return kw


class CourseDetail(DetailView):
    model = Course
    template_name = 'tasks/course_detail.html'
    context_object_name = 'course'

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().is_published and self.get_object().owner != request.user:
            return redirect('tasks:course_list')
        return super(CourseDetail, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['subscribes'] = Course.objects.filter(subscribes__owner=self.request.user)

        return context


class CourseList(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'tasks/course_list.html'

    def get_queryset(self):
        if self.request.user.is_teacher:
            return Course.objects.filter(owner=self.request.user)
        else:
             # Subscribes.objects.filter(owner=self.request.user)
            return Course.objects.filter(subscribes__owner=self.request.user, is_published=True)
    

class TaskCreate(CreateView):
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    model = Task


    def get_success_url(self, **kwargs):         
        return reverse_lazy("tasks:view_task", kwargs={'pk': kwargs['pk'], 'course_id':kwargs['course_id']})
        

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            return redirect('tasks:task_list', course_id=kwargs['course_id'])

        course = get_object_or_404(Course, pk=kwargs['course_id'])
        
        if course.owner != request.user:
            return redirect('tasks:task_list', course_id=kwargs['course_id'])

        return super(TaskCreate, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.owner = self.request.user

        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        form.instance.course = course

        if 'is_published' in form.cleaned_data and form.cleaned_data['is_published'] == 'on':
            form.instance.published_date = timezone.now()
        task = form.save() 

        return HttpResponseRedirect(self.get_success_url(pk=task.pk, course_id=course.pk))

    def get_form_kwargs(self):
        kw = super(TaskCreate, self).get_form_kwargs()
        kw['request'] = self.request
        kw['kw'] = self.kwargs
        return kw

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=self.kwargs['course_id'])

        return context


class TaskUpdate(UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    form_class = TaskForm

    def get_success_url(self, **kwargs):         
        return reverse_lazy("tasks:view_task", kwargs={'pk': self.get_object().pk, 'course_id':kwargs['course_id']})


    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            return redirect('tasks:view_task', pk=kwargs['pk'], course_id=kwargs['course_id'])
        return super(TaskUpdate, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        task = form.save() 
        return HttpResponseRedirect(self.get_success_url(pk=task.pk, course_id=task.course.pk))


    def get_form_kwargs(self):
        kw = super(TaskUpdate, self).get_form_kwargs()
        kw['request'] = self.request
        kw['kw'] = self.kwargs
        return kw


class TaskDetail(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().is_published and self.get_object().owner != request.user:
            return redirect('tasks:view_task', pk=kwargs['pk'], course_id=kwargs['course_id'])

        if request.user.is_teacher:
            self.template_name = 'tasks/task_detail_teacher.html'

        return super(TaskDetail, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        context['progress'] = Progress.objects.filter(owner=self.request.user, course=course)
        context['tasks'] = Task.objects.filter(course=course)
        context['doneTasksLen'] = Progress.objects.filter(owner=self.request.user, course=course, is_passed=True)
        return context


class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        if self.request.user == course.owner:
            return Task.objects.filter(owner=self.request.user, course=course)
        else:
            return Task.objects.filter(owner=self.request.user, course=course, is_published=True)   

        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        context['course'] = course
        return context


class Subscribe(View):

    def dispatch(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        res = 'FAIL'
        if not request.user.is_teacher and course.is_published:
            progress, created = Subscribes.objects.get_or_create(owner=request.user, course=course)
            if created:
                res = 'OK'
        return JsonResponse({'result': res}) 


class Unsubscribe(View):

    def dispatch(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        res = 'FAIL'
        if not request.user.is_teacher and course.is_published:
            progress = get_object_or_404(Subscribes, owner=request.user, course=course)
            if progress != None:
                progress.delete()
                res = 'OK'
        return JsonResponse({'result': res}) 


class GlobalCourseList(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'tasks/global_course_list.html'

    def get_queryset(self):
        return Course.objects.filter(is_published=True)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscribes'] = Course.objects.filter(subscribes__owner=self.request.user)
        return context


class ToggleLike(View):
    def dispatch(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        res = 'FAIL'
        if course.is_published:
            like, created = Like.objects.get_or_create(owner=request.user, course=course)
            if created:
                like.delete()
                res = 'DELETED'
            else:
                like.save()
                res = 'LIKED'

        return JsonResponse({'result': res})  


class DatabaseCreate(CreateView):
    template_name = "tasks/db_form.html"
    form_class = DataBaseForm
    model = Task_db


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            return redirect('tasks:course_list')
        return super(DatabaseCreate, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.staffname = str(self.request.user.pk)+'_'+str(int(timezone.now().timestamp()))+'_'+form.cleaned_data['dbname']
        
        manager = DBManager()
        manager.create_db(form.instance.staffname)
        manager.close()

        form.save() 

        return super(DatabaseCreate, self).form_valid(form)

    def get_form_kwargs(self):
        kw = super(DatabaseCreate, self).get_form_kwargs()
        kw['request'] = self.request
        kw['kw'] = self.kwargs
        return kw


class TableCreate(CreateView):
    template_name = "tasks/table_form.html"
    form_class = TableForm
    model = Task_table


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            return redirect('tasks:course_list')
        return super(TableCreate, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.staffname = str(self.request.user.pk)+'_'+str(int(timezone.now().timestamp()))+'_'+form.cleaned_data['name']
        form.instance.db = form.cleaned_data['db']

        query = form.cleaned_data['create_query'].replace(form.cleaned_data['name'], form.instance.staffname, 1)
        data_query = form.cleaned_data['data_query'].replace(form.cleaned_data['name'], form.instance.staffname, 1)
        manager = DBManager()
        manager.use_db(form.cleaned_data['db'].staffname)
        manager.create_table(query)
        manager.exec(data_query)
        manager.close()

        form.save() 

        return super(TableCreate, self).form_valid(form)

    def get_form_kwargs(self):
        kw = super(TableCreate, self).get_form_kwargs()
        kw['request'] = self.request
        kw['kw'] = self.kwargs
        return kw


class TestMysql(View):
    def dispatch(self, request, *args, **kwargs):
        manager = DBManager()
        manager.create_db('test_db')
        manager.use_db('test_db')
        manager.create_table("CREATE TABLE t1 (c1 INT STORAGE DISK, c2 INT STORAGE MEMORY)")
        manager.exec("INSERT INTO t1 (c1, c2) values (1, 2), (3, 4)")
        rows = manager.get_rows("SELECT * FROM t1")
        manager.close()

        return HttpResponse(str(rows))
        


class TableDetail(DetailView):
    model = Task_table
    template_name = 'tasks/table_detail.html'
    context_object_name = 'table'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            return redirect('tasks:course_list')
        return super(TableDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.get_object()
        table_name = table.staffname
        db_name = table.db.staffname

        manager = DBManager()
        manager.use_db(db_name)

        rows = manager.get_rows("select * from {} limit 25".format(table_name))
        field_names = [i[0] for i in manager.get_cursor().description]


        context['rows'] = rows
        context['field_names'] = field_names

        manager.close()

        return context


class DatabaseDetail(DetailView):
    model = Task_db
    template_name = 'tasks/db_detail.html'
    context_object_name = 'db'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            return redirect('tasks:course_list')
        return super(DatabaseDetail, self).dispatch(request, *args, **kwargs)