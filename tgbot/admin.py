from django.contrib import admin

from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'telegram',
        'name',
    )

admin.site.register(Developer)
admin.site.register(Manager)
admin.site.register(Owner)
admin.site.register(Tariff)
