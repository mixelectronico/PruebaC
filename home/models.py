from django.db import models

from login.models import User


class Trip(models.Model):
    creator = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE)
    destination = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField()
    trip_plan = models.CharField(max_length=40)
    joined_user = models.ManyToManyField(User, related_name="users", blank=True, null=True)