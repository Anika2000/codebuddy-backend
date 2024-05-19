# models.py    
from django.db import models

class CollaborationSession(models.Model):
    room_id = models.CharField(max_length=100, unique=True)
    created_by = models.CharField(max_length=100)  # Store user ID as a string
    participants = models.JSONField(default=list)  # Store participant user IDs as a list of strings

    def __str__(self):
        return f'Room {self.room_id} created by {self.created_by}'

