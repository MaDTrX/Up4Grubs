from dataclasses import field
from django.shortcuts import render
from .models import Grub 
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

# Create your views here.
from django.http import HttpResponse
#* Used as a retrun object from a django view


# Define the home view
def home(request):
    grubs = Grub.objects.all()
    # console.log(grubs)
#     #* gets all grubs| class Grub is imported from models
    return render(request, 'home.html',{'grubs': grubs} )
#     #! define  a function called grubs

def about(request):
    return render(request, 'about.html')

class GrubList(ListView):
    model = Grub
    
class GrubCreate(CreateView):
    model = Grub
    fields = '__all__'
    success_url = '/grubs/'

class GrubDelete(DeleteView):
    model = Grub
    success_url = '/grubs/'

class GrubDetail(DetailView):
    model = Grub

class GrubUpdate(UpdateView):
    model = Grub 
    fields = '__all__'
    success_url = '/grubs/'
    # find a way to attach the id at the end of success url


