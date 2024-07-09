from django.contrib import admin
from .models import *


class employeeAdmin(admin.ModelAdmin):
    list_display = ('name','email')

class eventAdmin(admin.ModelAdmin):
    list_display = ('employee','event_type','event_date')

class emailTemplateAdmin(admin.ModelAdmin):
    list_display = ('event_type','email_subject','email_content')

class emailLogsAdmin(admin.ModelAdmin):
    list_display = ('event','status','error_message')

class djangoLogsAdmin(admin.ModelAdmin):
    list_display = ('status','logs','date')


admin.site.register(Employee,employeeAdmin)
admin.site.register(Event,eventAdmin)
admin.site.register(EmailTemplate,emailTemplateAdmin)
admin.site.register(EmailLogs,emailLogsAdmin)
admin.site.register(DjangoLogs,djangoLogsAdmin)

