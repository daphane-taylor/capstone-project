from django.contrib import admin
from .models import Item, CollectionComment, Activity
# Register your models here.
admin.site.register(Item)
admin.site.register(CollectionComment)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'item', 'timestamp')
    list_filter = ('activity_type', 'timestamp')
    search_fields = ('user__username', 'item__name')
    date_hierarchy = 'timestamp'

admin.site.register(Activity, ActivityAdmin)

