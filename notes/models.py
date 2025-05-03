from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='notes/images/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title



class NoteActivity(models.Model):
    ACTIVITY_TYPES =(
        ('create', 'Created new note'),
        ('view', 'Viewed note details'),
        ('delete', 'Deleted note'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"{self.user.username} {self.get_activity_type_display()}: {self.note.title}"