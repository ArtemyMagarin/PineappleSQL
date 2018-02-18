from django.shortcuts import render_to_response
from einvite.forms import InviteListForm

from django.core.mail import send_mail

from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render_to_response

from .forms import InviteListForm

from .models import Invite
from tasks.models import Course

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse

from django.utils.translation import ugettext_lazy as _


# class InviteView(CreateView):
#     template_name = 'invite/invite_students.html'
#     form_class = InviteListForm
#     # model = User
#     success_url=reverse_lazy("accounts:thanks")

#     def form_valid(self, form):
#         current_site = get_current_site(self.request)
# 		user = form.save()
# 		mail_subject = 'Приглашение на курс в Pineapple-SQL'
# 		message = render_to_string('acc_active_email.html', {
# 			'user': user,
# 			'course': course,
# 			'domain': current_site.domain,
# 			'uid': str(urlsafe_base64_encode(force_bytes(user.pk)))[2:-1],
# 			'token':account_activation_token.make_token(user),
# 		})
# 		to_email = parse_email(form.cleaned_data['emails'])
# 		email = EmailMessage(mail_subject, message, to=to_email)
# 		email.send()

#         return super(UserCreateView, self).form_valid(form)

def invites(request, *args, **kwargs):
	course = Course.objects.get(pk=kwargs['course_id'])
	course_name = course.name
	if request.method == 'POST':
		form = InviteListForm(request.POST)
		if form.is_valid():
			current_site = get_current_site(request)
			user = request.user
			mail_subject = 'Приглашение на курс в Pineapple-SQL'
			message = render_to_string('invite_email.html', {
				'user': user,
				'course': course,
				'domain': current_site.domain,				
			})
			to_email = parse_email(form.cleaned_data['emails'])
			email = EmailMessage(mail_subject, message, to=to_email)
			email.send()
			for email in to_email:
				if not Invite.objects.filter(course=course,emails=email):	
					inv = Invite(emails = email, course = course)
					inv.save()
			return render(request, 'invite/thanks.html', {'header': "Студнты успешно приглашены", 'a': "Вернуться на страницу курса", 'pk': kwargs['course_id']})
	else:       
		form = InviteListForm()
	return render(request, 'invite/invite_students.html', {'form': form, 'user': request.user, 'course_name': course_name})

def parse_email(e_string):
	return e_string.split(' ')

def thanks(request):
	return render_to_response('registration/thanks.html', {'header': "Спасибо за регистрацию!", 'p': "Проверьте свой почтовый ящик :-)"})
