from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name



class Event(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=255)
    event_date = models.DateField()

    def __str__(self):
        return self.event_type


class EmailTemplate(models.Model):
    event_type = models.CharField(max_length=255)
    email_subject = models.CharField(max_length=255)
    email_content = models.TextField()


class EmailLogs(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    error_message = models.TextField()


class DjangoLogs(models.Model):
    status = models.CharField(max_length=20)
    logs = models.TextField()
    date = models.DateField()
    
