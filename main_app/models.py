from email.policy import default
from django.db import models
from datetime import date
import datetime
from django.urls import reverse
#import timedelta
from django.contrib.auth.models import User

TYPE = (
    ('Fresh Produce', 'Fresh'),
    ('Pantry', 'Pantry')
)
# Create your models here.
class Grub(models.Model):
    item =  models.CharField(
        max_length=50,
        default='Enter Item')
    type = models.CharField(
        max_length = 50,
        choices = TYPE,
        default= TYPE[0][0]
    )
    exp: models.DateField(
        'exp date'
        # default=
        #* set exp date to 3 days after the created date
        )
    #TODO set default date
    # photo: models.BinaryField
    desc =  models.TextField(
        max_length=250,
        default = 'Enter Description')
    price = models.IntegerField(
        default=0
    )
    user = models.ForeignKey(User,  on_delete=models.CASCADE)

    def __str__(self):
       return self.item
