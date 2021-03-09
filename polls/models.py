from django.db import models
from django.utils import timezone
import uuid
# Create your models here.



class Record(models.Model):
    user = models.CharField(max_length=50,default='',null=True,blank=True)
    kill = models.IntegerField()
    death = models.IntegerField()
    score = models.IntegerField()
    DateTime = models.DateTimeField(default=timezone.now)
