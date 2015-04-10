from django.db import models

# Create your models here.
class SampleCount(models.Model):
	text = models.CharField(max_length=500)