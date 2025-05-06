from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Collection(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def item_count(self):
        return self.items.count()

ACTIVITY_TYPES = (
    ('create', 'Created new item'),
    ('view', 'Viewed item details'),
    ('delete', 'Deleted item'),
    ('add_to_collection', 'Added item to collection'),
    ('remove_from_collection', 'Removed item from collection'),
)