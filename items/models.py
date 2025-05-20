from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from categories.models import Collection  

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=200)
    other_names = models.CharField(max_length=300, blank=True, null=True)
    date_collected = models.DateField()
    value = models.CharField(max_length=20)
    vendor = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100)
    size = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    collections = models.ManyToManyField(Collection, blank=True, related_name='items')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name


class CollectionComment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name + " - " + self.content[0:40]


class Activity(models.Model):
    ACTIVITY_TYPES = (
        ('create', 'Created new item'),
        ('view', 'Viewed item details'),
        ('delete', 'Deleted item'),
        ('add_to_collection', 'Added item to collection'),
        ('remove_from_collection', 'Removed item from collection'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=25, choices=ACTIVITY_TYPES)
    timestamp = models.DateTimeField(default=timezone.now)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        base_str = f"{self.user.username} {self.get_activity_type_display()}: {self.item.name}"
        if self.collection and self.activity_type in ['add_to_collection', 'remove_from_collection']:
            return f"{base_str} in collection '{self.collection.name}'"
        return base_str