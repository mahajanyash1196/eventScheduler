from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .tasks import send_event_emails

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        send_event_emails()
        return JsonResponse('Email task is scheduled.',status = status.HTTP_202_ACCEPTED,safe=False)
    else:
        return JsonResponse('Not Allowed',status=status.HTTP_405_METHOD_NOT_ALLOWED,safe=False)
