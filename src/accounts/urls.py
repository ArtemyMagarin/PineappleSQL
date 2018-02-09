from django.urls import path, re_path

from django.contrib.auth import views as auth_views
from .views import UserCreateView, UserUpdateView, activate, UserDetailView, thanks
from .views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeDoneView, PasswordChangeView, LoginView, LogoutView

from django.urls import reverse_lazy

app_name = 'accounts'


urlpatterns = [

    path('register/', UserCreateView.as_view(), name='register'),
    path('thanks/', thanks, name='thanks'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    path('edit/', UserUpdateView.as_view(), name="edit"),
    path('', UserDetailView.as_view(), name="profile" ),

    re_path(r'^password_reset/$', PasswordResetView.as_view(), name='password_reset'),
    re_path(r'^password_reset/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^reset/done/$', PasswordResetCompleteView.as_view(), name='password_reset_complete', ),
    re_path(r'^password_change/$', PasswordChangeView.as_view(), name="password_change"),
    re_path(r'^password_change/done/$', PasswordChangeDoneView.as_view(), name="password_change_done"),

]
