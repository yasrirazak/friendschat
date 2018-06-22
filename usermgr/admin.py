from django.contrib import admin
from usermgr.models import Messages,Friends,Status,User
class FriendsInline(admin.StackedInline):
    model = Friends
    extra = 1
class StatusInline(admin.StackedInline):
    model = Status
    extra = 1
class MessagesInline(admin.StackedInline):
    model = Messages
    extra = 1
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
    (None, {'fields': ['username']}),
    ('Password information', {'fields': ['password'],'classes': ['collapse']}),
    ]
    inlines = [StatusInline,FriendsInline,MessagesInline]
admin.site.register(User, UserAdmin)
