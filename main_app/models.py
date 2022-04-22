from django.contrib.auth.models import User
from email.policy import default
from django.urls import reverse
from django.db import models


TYPE = (
    ('Fresh Produce', 'Fresh'),
    ('Pantry', 'Pantry')
)

OPTION = (
    ('Pick-up', 'Pick-Up'),
    ('Delivery', 'Delivery')
)

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
    exp = models.DateField(
        'exp date',
         blank = True,
         null = True
    )
  
    desc =  models.TextField(
        max_length=250,
        blank = True, 
        null = True
    )
    option = models.CharField(
        max_length=10,
        choices=OPTION,
        default=OPTION[0][0]
    )
    location = models.CharField(
        max_length=200,
         blank = True, 
         null = True
    )
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    def __str__(self):
       return self.item
    #    f'Photo for grub_id: {self.user} @{self.url}'

    def get_absolute_url(self):
        return reverse('grubs_detail', kwargs={'pk': self.id})

class Photo(models.Model):
    grub = models.ForeignKey(Grub,  on_delete=models.CASCADE, blank = True, 
         null = True)
    url = models.FileField(
        blank = True, 
        null = True,
    )
class Claim(models.Model):
    grub = models.ForeignKey(Grub, on_delete=models.CASCADE, blank = True, null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)