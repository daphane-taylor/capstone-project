from django.contrib import admin
from .models import ContactMessage

# Register your models here.
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'timestamp')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', ('phone', 'extension', 'phone_type'))
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('System Information', {
            'fields': ('timestamp',)
        }),
    )

admin.site.register(ContactMessage, ContactMessageAdmin)