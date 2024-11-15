# models.py
from django.db import models
from django.contrib.auth.models import User

class ChatLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'

class SymptomTip(models.Model):
    symptom = models.CharField(max_length=255)
    tip = models.TextField()

    def __str__(self):
        return self.symptom
