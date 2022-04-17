from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Grub 
from dataclasses import field

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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class GrubList(ListView):
    model = Grub
    
class GrubDetail(LoginRequiredMixin, DetailView):
    model = Grub

class GrubCreate(LoginRequiredMixin, CreateView):
    model = Grub
    fields = '__all__'
    success_url = '/grubs/'
    def form_valid(self, form):
    # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the grub
    # Let the CreateView do its job as usual
        return super().form_valid(form)

class GrubUpdate(LoginRequiredMixin, UpdateView):
    model = Grub 
    fields = '__all__'
    success_url = '/grubs/'
    # find a way to attach the id at the end of success url

class GrubDelete(LoginRequiredMixin, DeleteView):
    model = Grub
    success_url = '/grubs/'

