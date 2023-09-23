from emailSender.models import *
from rest_framework import serializers


class employeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('name','email','created_at')

class eventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('employee','event_type','event_date','created_at')

class emailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ('event_type','email_subject','email_content')

class emailLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailLogs
        fields = ('event','status','error_message')

class djangoLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoLogs
        fields = ('status','logs','date')
