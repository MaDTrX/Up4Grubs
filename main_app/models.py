from email.policy import default
from django.db import models
from datetime import date
import datetime
#import timedelta
from django.contrib.auth.models import User

TYPE = (
    ('F','Fresh Produce'),
    ('P','pantry')
)
# Create your models here.
class Grub(models.Model):
    item =  models.CharField(max_length=50)
    type = models.CharField(
        max_length = 1,
        choices = TYPE,
    )

    exp = models.DateField(
        'exp date', 
         #! + timedelta(days=7)
        #* set exp date to 3 days after the created date
        )
    #TODO set default date
    # photo: models.BinaryField
    desc =  models.TextField(max_length=250)
    price = models.IntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
       return self.type
