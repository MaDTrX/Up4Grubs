from email.policy import default
from django.db import models

TYPE = (
    ('F','Fresh Produce'),
    ('P','pantry')
)
# Create your models here.
class Grub(models.Model):
    type: models.CharField(
        max_length = 1,
        choices = TYPE,
    )
    def __str__(self):
       return self.type

class Fresh(models.Model):
    exp: models.DateField(
        'exp date'
        # default=
        #* set exp date to 3 days after the created date
        )
    #TODO set default date
    # photo: models.BinaryField
    desc: models.TextField(max_length = 250)
    price: models.IntegerField()

class Pantry(models.Model):
    exp: models.DateField('exp date')
    # photo: models.BinaryField
    desc: models.TextField(max_length = 250)
    price: models.IntegerField()


    def __str__(self):
       return self.exp
