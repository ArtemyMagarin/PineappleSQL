from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from tasks.models import Course

class Invite(models.Model):
	emails = models.CharField(max_length=1000, null=False)
	course = models.ForeignKey(
		'tasks.Course',
		related_name='invites',
		null=False, blank=False,
		on_delete=models.PROTECT
	)
