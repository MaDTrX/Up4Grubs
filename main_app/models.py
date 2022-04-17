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
<<<<<<< Updated upstream

    exp = models.DateField(
        'exp date', 
        default= 2022-11-23
         #! + timedelta(days=7)  
=======
    exp = models.IntegerField(
        'exp date',
         default= 2022
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    
    def get_absolute_url(self):
        return reverse("grubs_detail", kwargs={"grub_id": self.id})
    


=======

    def get_absolute_url(self):
        return reverse('detail', kwargs={'grub_id': self.id})
class Photo (models.Model):
    url = models.CharField(max_length=200)
    grub = models.ForeignKey(Grub, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for grub_id: {self.grub_id} @{self.url}'
>>>>>>> Stashed changes
