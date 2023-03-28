from django.db import models

class FloorPlan(models.Model):
    name = models.CharField(max_length=1000)
    file = models.FileField(upload_to='floorplans/')

class Dimension(models.Model):
    file_type = models.CharField(max_length=10)
    file_path = models.CharField(max_length=200)
    length = models.FloatField()
    width = models.FloatField()
    flow_ratio = models.FloatField()

