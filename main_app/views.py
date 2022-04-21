from django.views.generic.edit import UpdateView, CreateView, DeleteView, DeletionMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.db.models.signals import post_delete
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Grub, Photo, Claim
from django.contrib.auth import login
from django.dispatch import receiver
from django.urls import reverse
from django.db.models import Q
import boto3
import uuid
import os

def home(request):
    claims = Claim.objects.all()
    grubs = Grub.objects.all()
    matches = []
    for claim in claims:
       matches.extend(grubs.exclude(~Q(id=claim.grub.id)))
    filter = []
    for el in grubs:
        if el not in matches:
            filter.append(el)
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
                s3 = boto3.client('s3')
                key = uuid.uuid4().hex[:6] + img.name[img.name.rfind('.'):]

                try:
                    bucket = os.environ['S3_BUCKET']
                    s3.upload_fileobj(img, bucket, key)
                    url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                    Photo.objects.create(url=url, grub=form.instance)
                    return HttpResponseRedirect(self.get_success_url())
                except Exception as e:
                    print('An error occurred uploading file to S3')
                    print(e)
                    return redirect('home')
            else: 
                print('Need to upload file')
        return HttpResponseRedirect(self.get_success_url())


class GrubUpdate(LoginRequiredMixin, UpdateView):
    model = Grub 
    fields = ['item','type','exp','desc', 'option', 'location']

    def get_context_data(self, **kwargs):
        places = super(GrubUpdate, self).get_context_data(**kwargs)
        places['places'] = os.environ.get('PLACES_API')
        return places

    def form_valid(self, form):
        super().form_valid(form) 
        photo_file = self.request.FILES.getlist('url', None)
        for img in photo_file:
            if img:
                s3 = boto3.client('s3')
                key = uuid.uuid4().hex[:6] + img.name[img.name.rfind('.'):]
                try:
                    bucket = os.environ['S3_BUCKET']
                    s3.upload_fileobj(img, bucket, key)
                    url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}" 
                    Photo.objects.create(url=url, grub=form.instance)
                    return HttpResponseRedirect(self.get_success_url())
                except Exception as e:
                    print('An error occurred uploading file to S3')
                    print(e)
                    return redirect('home')
            else: 
                print('Need to upload file')
        return HttpResponseRedirect(self.get_success_url())
    

class GrubDelete(LoginRequiredMixin, DeleteView):
    model = Grub
    success_url = '/index/'

class ClaimCreate(LoginRequiredMixin, CreateView):
    model = Claim
    success_url = '/index/'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        grub = Grub.objects.filter(id=self.request.GET.get('id', None))
        claim = Claim.objects.filter(grub=None, user=self.request.user)
        claim.update(grub=grub[0])
        return redirect('/grubs/')

class PhotoDelete(LoginRequiredMixin, DeleteView):
    model = Photo
    def delete(self, request, pk):
        s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
        url = self.request.GET.get("url", None)
        redirect = self.request.GET.get("id", None)
        img_id = self.request.GET.get("img", None)
        img = url[-10:]
        photo_delete = Photo.objects.get(id=img_id)
        photo_delete.delete()
        deleted = s3.delete_object(Bucket=os.environ['S3_BUCKET'], Key=img)
        @receiver(post_delete, sender=Photo)
        def delete_image_file(sender, instance, **kwargs):                          
            instance.main_image.delete(False)
        return HttpResponseRedirect(reverse('grubs_detail', kwargs={'pk':redirect}))