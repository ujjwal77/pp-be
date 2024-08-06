from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    def __str__(self):
        return self.username

class Message(models.Model):   
    username = models.CharField(max_length=100)
    messages = models.TextField()

    def __str__(self):
        return f'{self.username}: {self.messages}'



class llm_messages(models.Model):
    username = models.CharField(max_length=255, unique=True)
    messages = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} - {self.messages}'



class ConversationHistory(models.Model):
    username = models.CharField(max_length=255, unique=True)
    messages = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    extra_responses = models.TextField()
    all_questions = models.TextField(null=True)

    def __str__(self):
        return f'{self.username} - {self.messages}'


class TranscribedAudio(models.Model):
    firstname = models.CharField(max_length=255)
    file = models.FileField(upload_to='audio_files/')
    transcribed_text = models.TextField(null=True, blank=True)

