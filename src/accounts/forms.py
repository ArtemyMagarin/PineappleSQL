from django import forms
from .models import User, Group

from django.utils.translation import ugettext_lazy as _


class UserCreateForm(forms.ModelForm):

    last_name = forms.CharField(max_length=100, required=True, label='Фамилия')
    first_name = forms.CharField(max_length=100, required=True, label='Имя')
    middle_name = forms.CharField(max_length=100, required=False, label='Отчество')
    groupNum = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="-----", label='Номер группы', required=False)
    email = forms.EmailField(required=True, label='E-Mail')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label='Повторите пароль')

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'middle_name', 'groupNum', 'email', 'password', 'password2')

    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            self.add_error('password2', forms.ValidationError(_("Пароли должны совпадать")))


class UserUpdateForm(forms.ModelForm):

    last_name = forms.CharField(max_length=100, required=True, label='Фамилия')
    first_name = forms.CharField(max_length=100, required=True, label='Имя')
    middle_name = forms.CharField(max_length=100, required=False, label='Отчество')
    groupNum = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="-----", label='Номер группы', required=False)
    email = forms.EmailField(required=True, label='E-Mail', disabled=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Пароль', help_text='Введите пароль, чтобы подтвердить изменения')

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'middle_name', 'groupNum', 'email', 'password')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserUpdateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(UserUpdateForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if self.request.user.email != email:
            self.add_error('email', forms.ValidationError(_("Вы не можете сменить email")))

        if not self.request.user.check_password(password):
            self.add_error('password', forms.ValidationError(_("Чтобы изменить данные аккаунта необходимо ввести корректный пароль")))   

        try:
            cleaned_data.pop('password')
        except Exception:
            pass

        return cleaned_data
