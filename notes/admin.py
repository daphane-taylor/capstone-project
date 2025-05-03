from django.contrib import admin
from .models import Note, NoteActivity

# Register your models here.
admin.site.register(Note)
admin.site.register(NoteActivity)