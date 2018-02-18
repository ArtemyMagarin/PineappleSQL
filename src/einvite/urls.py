from django.urls import path, re_path

from django.contrib.auth import views as auth_views
from .views import invites

from django.urls import reverse_lazy

app_name = 'einvite'


urlpatterns = [

    #path('', invites, name='invite_students'),    


]
