from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    description = models.TextField()
    place = models.CharField(max_length=255)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    nearby_hospitals = models.CharField(max_length=255)
    nearby_colleges = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    likes = models.ManyToManyField(User, related_name='liked_properties', blank=True)

class InterestedBuyer(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='interested_buyers')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    contacted = models.BooleanField(default=False)