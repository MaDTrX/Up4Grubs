from django.shortcuts import render
from .models import Grub 

# Create your views here.
from django.http import HttpResponse
#* Used as a retrun object from a django view


# Define the home view
def home(request):
    # grubs = Grub.objects.all()
    # console.log(grubs)
#     #* gets all grubs| class Grub is imported from models
    return render(request, 'home.html')
#     #! define  a function called grubs

def about(request):
    return render(request, 'about.html')

