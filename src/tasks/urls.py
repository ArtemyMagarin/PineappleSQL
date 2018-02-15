from django.urls import path, re_path
from .views import CourseList, CourseCreate, CourseDetail, CourseUpdate, GlobalCourseList
from .views import TaskList, TaskCreate, TaskDetail, TaskUpdate
from .views import Subscribe, Unsubscribe, ToggleLike

app_name = 'tasks'


urlpatterns = [

    path('all/', GlobalCourseList.as_view(), name='global_course_list'),

    path('', CourseList.as_view(), name='course_list'),
    path('new/', CourseCreate.as_view(), name='create_course'),
    path('<int:pk>/', CourseDetail.as_view(), name='view_course'),
    path('<int:pk>/like', ToggleLike.as_view(), name='like_course'),
    path('<int:pk>/edit/', CourseUpdate.as_view(), name='update_course'),

    path('<int:course_id>/tasks/', TaskList.as_view(), name='task_list'),
    path('<int:course_id>/tasks/new/', TaskCreate.as_view(), name='create_task'),
    path('<int:course_id>/tasks/<int:pk>/', TaskDetail.as_view(), name='view_task'),
    path('<int:course_id>/tasks/<int:pk>/edit/', TaskUpdate.as_view(), name='update_task'),

    path('<int:pk>/subscribe/', Subscribe.as_view(), name="course_subscribe"),
    path('<int:pk>/unsubscribe/', Unsubscribe.as_view(), name="course_unsubscribe"),

]