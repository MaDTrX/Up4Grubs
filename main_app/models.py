from email.policy import default
from django.db import models
from datetime import date
import datetime
from django.urls import reverse
#import timedelta
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

TYPE = (
    ('Fresh Produce', 'Fresh'),
    ('Pantry', 'Pantry')
)
# Create your models here.
OPTION = (
    ('P', 'Pick-Up'),
    ('D', 'Delivery')
)
# Create your models here.
class Grub(models.Model):
    item =  models.CharField(
        max_length=50,
        blank = True, 
        null = True
       )
    type = models.CharField(
        max_length = 50,
        choices = TYPE,
        default= TYPE[0][0]
        )
    exp = models.IntegerField(
        'exp date',
         blank = True, 
         null = True
        #* set exp date to 3 days after the created date
        )
    #TODO set default date
    # photo: models.BinaryField
    desc =  models.TextField(
        max_length=250,
         blank = True, 
         null = True
         )
    price = models.IntegerField(
         blank = True, 
         null = True
        )
    option = models.CharField(
        max_length=1,
        choices=OPTION,
        default=OPTION[0][0]
        )
    location = models.CharField(
        max_length=200,
         blank = True, 
         null = True
        )
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    url = ArrayField(
        models.FileField(
        max_length=200, 
        blank = True, 
        null = True,
        ),
        size = 5, 
        )

    def __str__(self):
       return self.item
    #    f'Photo for grub_id: {self.user} @{self.url}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'grub_id': self.id})
      


