from celery import shared_task
from django.core.cache import cache

from emailSender.models import *
from emailSender.serializers import *

import datetime
import requests


def send_mail(mail_sender,recipient_sender,emailSubject,emailContent):
    print(mail_sender,recipient_sender,emailSubject,emailContent)

    # WE CAN WRITE ANY PYTHON SCRIPTS HERE TO SEND EMAILS FOR EXAMPLE SEND EMAILS VIA AWS OR SMTP
    
    try:
        return True
    except Exception as e:
        return False
    
def send_event_emails():

    last_successful_execution_time = cache.get('last_successful_execution_time')
    print("last_successful_execution_time =",last_successful_execution_time)

    today_date = datetime.datetime.now().date()
    

    # Check if the task should run based on the last successful execution time
    if last_successful_execution_time is None or last_successful_execution_time < today_date:


        if Event.objects.filter(event_date = today_date).exists():

            events = Event.objects.filter(event_date = today_date)

            for event in events:
                employee = event.employee
                eventType = event.event_type

                template = EmailTemplate.objects.get(event_type = eventType)
                
                emailSubject = template.email_subject
                emailContent = f"{template.email_content} {employee.name}"

                print('Mail Subject =',emailSubject)
                print('Mail Body =',emailContent)

                # WE CAN SEND MAILS BY AWS OR SMTP PYTHON SCRIPTS
                # FOR THESE I NEED CREDENTIALS WHICH I DONT HAVE

                mail_sender = 'abc@gmail.com'
                recipient_sender = employee.email

                retry_count = 0
                mail_response = False

                # TRIGGERING EMAIL SENT FOR 3 TIMES IF EMAIL DOES NOT SENT
                while retry_count < 3 and not mail_response:

                    try:
                        mail_repsonse = send_mail(mail_sender,recipient_sender,emailSubject,emailContent)

                        if mail_repsonse == True:
                            break
                        else:
                            retry_count += 1

                    except Exception as e:
                        retry_count += 1

                if mail_repsonse:

                    logs_data = {}
                    logs_data['event'] = event.id
                    logs_data['status'] = 'Sent'
                    logs_data['error_message'] = 'No Error,Mail sent'

                    email_logs = emailLogsSerializer(data = logs_data)
                    if email_logs.is_valid(raise_exception=True):
                        email_logs.save()
                    
                # EVEN AFTER TRYING FOR THREE TIMES EMAIL DOES NOT SEND THEN SAVING LOGS STATUS TO FAILED
                else:
                    print(f"tried for 3 times still email sent failed")
                    logs_data = {}
                    logs_data['event'] = event.id
                    logs_data['status'] = 'Failed'
                    logs_data['error_message'] = 'Max Retry Reaches'

                    email_logs = emailLogsSerializer(data = logs_data)
                    if email_logs.is_valid(raise_exception=True):
                        email_logs.save()

            # Events are scheduled          
            djangoLogs_data = {}
            djangoLogs_data['status'] = 'Success'
            djangoLogs_data['logs'] = 'Event are scheduled'
            djangoLogs_data['date'] = today_date

            django_logs = djangoLogsSerializer(data = djangoLogs_data)
            if django_logs.is_valid(raise_exception=True):
                django_logs.save()
        else:
            # NO Event are Scheduled
            djangoLogs_data = {}
            djangoLogs_data['status'] = 'Failed'
            djangoLogs_data['logs'] = 'No event are scheduled'
            djangoLogs_data['date'] = today_date

            django_logs = djangoLogsSerializer(data = djangoLogs_data)
            if django_logs.is_valid(raise_exception=True):
                django_logs.save()
        
        # Update last_successful_execution_time when the task is successfully completed
        cache.set('last_successful_execution_time', today_date, None)
        

@shared_task
def trigger_event_email_task():
    try:
        # POST request to API endpoint
        response = requests.post('http://127.0.0.1:8000/send/email')
        response.raise_for_status()  # Raise an exception for any HTTP error
        return response.text 
    except Exception as e:
        raise e