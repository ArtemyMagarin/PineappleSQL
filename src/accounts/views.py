from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView, LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render_to_response

from django.forms import ValidationError


from .models import User
from .forms import UserCreateForm, UserUpdateForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse

from django.utils.translation import ugettext_lazy as _

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreateForm
    model = User
    success_url=reverse_lazy("accounts:thanks")

    def form_valid(self, form):
        form.instance.set_password(self.request.POST['password'])
        user = form.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Активируйте Ваш аккаунт на TonikSQL'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': str(urlsafe_base64_encode(force_bytes(user.pk)))[2:-1],
            'token':account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return super(UserCreateView, self).form_valid(form)

def thanks(request):
    return render_to_response('registration/thanks.html', {'header': "Спасибо за регистрацию!", 'p': "Проверьте свой почтовый ящик :-)"})
    
        


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/edit.html'
    form_class = UserUpdateForm
    model = User

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy("accounts:edit")

    def get_form_kwargs(self):
        kw = super(UserUpdateView, self).get_form_kwargs()
        kw['request'] = self.request
        return kw

    def form_valid(self, form):
        form.save()
        return super(UserUpdateView, self).form_valid(form)
      

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'registration/detail.html'
    context_object_name = 'user' 

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
        print(user.email)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render_to_response('registration/thanks.html', {'header': "Ваш аккаунт подтвержден!", 'p': "Теперь вы можете <a href='/'>войти</a> на сайт"})
    else:
        return render_to_response('registration/thanks.html', {'header': "Ошибка!", 'p': "Код невалиден. Попробуйте снова"})



class IndexLoginView(LoginView):
    template_name = 'registration/index.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        return reverse_lazy('accounts:profile')

    def form_invalid(self, form):
        return redirect(reverse_lazy('accounts:login'))


class LoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        return reverse_lazy('accounts:profile')


class LogoutView(LogoutView):
    next_page = reverse_lazy('index')



class PasswordResetView(PasswordResetView):
    success_url = reverse_lazy('accounts:password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Сброс пароля')

class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'
    title = _('Сброс пароля')

class PasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = _('Придумайте новый пароль')

class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Пароль успешно изменен!')

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'registration/password_change_form.html'
    title = False

class PasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_form.html'
    title = _('Пароль успешно изменен!')
