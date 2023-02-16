from django.contrib import admin

from .models import User, Developer, Manager, Owner

admin.site.register(User)
admin.site.register(Developer)
admin.site.register(Manager)
admin.site.register(Owner)
