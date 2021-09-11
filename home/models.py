from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.timezone import make_aware

from login.models import User


class TripManager(models.Manager):
    def basic_validator(self, postData):
        today = make_aware(timezone.now().today())

        errores = {}
        if len(postData['destination']) == 0:
            errores['destination'] = "Destination field cannot be empty"

        if len(postData['description']) == 0:
            errores['description'] = "Description field cannot be empty"

        if len(postData['start_date']) == 0:
            errores['start_date'] = "Starting travel date field cannot be empty"
            if len(postData['end_date']) == 0:
                errores['end_date'] = "Ending travel date field cannot be empty"
        else:
            start_date = make_aware(datetime.strptime(postData['start_date'], '%Y-%m-%d'))
            if start_date <= today:
                errores['start_date'] = "The starting date must be in the future"

            if len(postData['end_date']) == 0:
                errores['end_date'] = "Ending travel date field cannot be empty"
            else:
                end_date = make_aware(datetime.strptime(postData['end_date'], '%Y-%m-%d'))
                if end_date <= start_date:
                    errores['end_date'] = "Ending travel date field cannot be before the starting date"

        return errores


class Trip(models.Model):
    creator = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE)
    destination = models.CharField(max_length=40)
    description = models.CharField(max_length=200, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField()
    # trip_plan = models.CharField(max_length=40)
    joined_user = models.ManyToManyField(User, related_name="users", blank=True, null=True)
    objects = TripManager()
