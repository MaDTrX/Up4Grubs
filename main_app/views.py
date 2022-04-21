
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Grub, Photo, Claim
from dataclasses import field
import boto3
import uuid
import os
import requests


# Define the home view
def home(request):
    claims = Claim.objects.all()
    grubs = Grub.objects.all()
    print(grubs)
    matches = []
    for claim in claims:
       matches.extend(grubs.exclude(~Q(id=claim.grub.id)))
    filter = []
    for el in grubs:
        if el not in matches:
            filter.append(el)
    print(filter, "test")
    #* gets all grubs| class Grub is imported from models
    return render(request, 'home.html', {'grubs': filter})

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

    def get_context_data(self, **kwargs):
        claim = super(GrubList, self).get_context_data(**kwargs)
        claim['claims'] = Claim.objects.filter(user=self.request.user)
        return claim    

    
class GrubDetail(LoginRequiredMixin, DetailView):
    model = Grub

    def get_context_data(self, **kwargs):
        photo = super(GrubDetail, self).get_context_data(**kwargs)
        photo['photo'] = Photo.objects.all()
        photo['places'] = os.environ.get('PLACES_API')
        return photo

class GrubCreate(LoginRequiredMixin, CreateView):
    model = Grub
    fields = ['item','type','exp','desc', 'option', 'location'] 
    success_url = '/grubs/'
    #! redirect to created grub
    def get_context_data(self, **kwargs):
        places = super(GrubCreate, self).get_context_data(**kwargs)
        places['places'] = os.environ.get('PLACES_API')
        return places
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form) 
        photo_file = self.request.FILES.getlist('url', None)
        for img in photo_file:
            if img:
                print(img)
                s3 = boto3.client('s3')
                key = uuid.uuid4().hex[:6] + img.name[img.name.rfind('.'):]

                try:
                    bucket = os.environ['S3_BUCKET']
                    s3.upload_fileobj(img, bucket, key)
                    # build the full url string
                    url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                    Photo.objects.create(url=url, grub=form.instance)

                except Exception as e:
                    print('An error occurred uploading file to S3')
                    print(e)
                    return redirect('home')
            else: 
                print('Need to upload file')
        
        return redirect('/grubs/')# Let the CreateView do its job as usual
        
    
class GrubUpdate(LoginRequiredMixin, UpdateView):
    model = Grub 
    fields = ['item','type','exp','desc', 'option', 'location']
    success_url = '/grubs/detail/5'
    #! redirect to update grub
    def form_valid(self, form):
        # form.instance.user = self.request.user 
        super().form_valid(form) # form.instance is the grub
  
        photo_file = self.request.FILES.getlist('url', None)
        print(form.instance.id)
        for img in photo_file:
        # photo-file will be the "name" attribute on the <input type="file">
            if img:
                print(img)
                s3 = boto3.client('s3')
                # need a unique "key" for S3 / needs image file extension too
                key = uuid.uuid4().hex[:6] + img.name[img.name.rfind('.'):]
                # just in case something goes wrong
                try:
                    bucket = os.environ['S3_BUCKET']
                    s3.upload_fileobj(img, bucket, key)
                    #! replicate for photo delete
                    # build the full url string
                    url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}" 

                    Photo.objects.create(url=url, grub=form.instance)
                    # we can assign to grub_id or cat (if you have a cat object)
                except Exception as e:
                    print('An error occurred uploading file to S3')
                    print(e)
                    return redirect('home')
            else: 
                print('Need to upload file')
                # Let the CreateView do its job as usual
        return redirect('/grubs/')
        # find a way to attach the id at the end of success url

class GrubDelete(LoginRequiredMixin, DeleteView):
    model = Grub
    success_url = '/grubs/'


class ClaimCreate(LoginRequiredMixin, CreateView):
    model = Claim
    success_url = '/grubs/'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        
        grub = Grub.objects.filter(id=self.request.GET.get('id', None))
        claim = Claim.objects.filter(grub=None, user=self.request.user)
        claim.update(grub=grub[0])
        return redirect('/grubs/')
      
