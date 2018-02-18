from django.contrib import admin
from .models import User, Group

class UserAdmin(admin.ModelAdmin):
	pass

class GroupAdmin(admin.ModelAdmin):
	pass


admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)