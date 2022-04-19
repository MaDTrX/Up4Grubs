
from operator import itemgetter
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Grub
from dataclasses import field
import boto3
import uuid
import os
import requests

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
    fields = ['item','type','exp','desc', 'price', 'option', 'location', 'url'] 
    success_url = '/grubs/'
    
    def form_valid(self, form):
        form.instance.user = self.request.user  # form.instance is the grub
        # Assign the logged in user (self.request.user)
        photo_file = self.request.FILES.get('url', None)
        # photo-file will be the "name" attribute on the <input type="file">
        if photo_file:
            s3 = boto3.client('s3')
            # need a unique "key" for S3 / needs image file extension too
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            # just in case something goes wrong
            try:
                bucket = os.environ['S3_BUCKET']
                s3.upload_fileobj(photo_file, bucket, key)
                # build the full url string
                form.instance.url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                # we can assign to grub_id or cat (if you have a cat object)
            except Exception as e:
                print('An error occurred uploading file to S3')
                print(e)
                return redirect('home')
        else: 
            print('Need to upload file')
            # Let the CreateView do its job as usual
        return super().form_valid(form)
    
class GrubUpdate(LoginRequiredMixin, UpdateView):
    def id(self):
        print(self.request.POST.get('url', None))
    model = Grub 
    fields = ['item','type','exp','desc', 'price', 'option', 'location', 'url']
    success_url = '/grubs/detail/5'
    def form_valid(self, form):
        print(self.request.FILES)
    # form.instance.user = self.request.user  # form.instance is the grub
    # Assign the logged in user (self.request.user)
        photo_file = self.request.FILES.get('url', None)
        for img in photo_file:
            print(img.name)
        # photo-file will be the "name" attribute on the <input type="file">
            if img:
                s3 = boto3.client('s3')
                # need a unique "key" for S3 / needs image file extension too
                key = uuid.uuid4().hex[:6] + img.name[img.name.rfind('.'):]
                # just in case something goes wrong
                try:
                    bucket = os.environ['S3_BUCKET']
                    s3.upload_fileobj(img, bucket, key)
                    # build the full url string
                    form.instance.url.append(f"{os.environ['S3_BASE_URL']}{bucket}/{key}")
                    # we can assign to grub_id or cat (if you have a cat object)
                except Exception as e:
                    print('An error occurred uploading file to S3')
                    print(e)
                    return redirect('home')
            else: 
                print('Need to upload file')
                # Let the CreateView do its job as usual
        return super().form_valid(form)
        # find a way to attach the id at the end of success url

class GrubDelete(LoginRequiredMixin, DeleteView):
    model = Grub
    success_url = '/grubs/'

