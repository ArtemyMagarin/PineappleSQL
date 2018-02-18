from django import forms
from .models import Invite

from django.utils.translation import ugettext_lazy as _


class InviteListForm(forms.ModelForm):
	emails = forms.CharField(widget=forms.Textarea(attrs=({'rows': 4, 'id': 'emaillist'})), max_length=10000, required=True, label='Список e-mail')

	def init(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(InviteListForm, self).init(*args, **kwargs)

	class Meta:
		model = Invite
		fields = ('emails',)
