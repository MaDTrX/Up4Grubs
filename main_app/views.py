from django.views.generic.edit import UpdateView, CreateView, DeleteView
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
    #* loops over the claims QuerySet
    for claim in claims:
    #*querying for grubs with a claim and pushing to matches(extend)
       matches.extend(grubs.exclude(~Q(id=claim.grub.id)))
    
    filter = []
    for grub in grubs:
        #* comparing grubs with matches and pushing non-matches to filter
        if grub not in matches:
            filter.append(grub)
            #* passing filter through the render to home for display
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
    #* using built-in django method to get some data
    def get_context_data(self, **kwargs):
        #* using super to access GrubList methods
        claim = super(GrubList, self).get_context_data(**kwargs)
        #* create key in proxy object tha hold a queryset value
        claim['claims'] = Claim.objects.filter(user=self.request.user)
        return claim    

    
class GrubDetail(LoginRequiredMixin, DetailView):
    model = Grub

    def get_context_data(self, **kwargs):
        photo = super(GrubDetail, self).get_context_data(**kwargs)
        #* create two keys in proxy object of photo and places with values of a Photo Model Queryset and place api key in .env respectively
        photo['photo'] = Photo.objects.all()
        photo['places'] = os.environ.get('PLACES_API')
        return photo

class GrubCreate(LoginRequiredMixin, CreateView):
    model = Grub
    #*list needed fields for create form
    fields = ['item','type','exp','desc', 'option', 'location'] 

    def get_context_data(self, **kwargs):
        places = super(GrubCreate, self).get_context_data(**kwargs)
        places['places'] = os.environ.get('PLACES_API')
        return places
    
    def form_valid(self, form):
        #*assign logged in user to user field in before submitting grub form instance
        form.instance.user = self.request.user
        #* save form before moving to the next step
        super().form_valid(form) 
        #*get Queryset list from client-side form
        photo_file = self.request.FILES.getlist('url', None)
        #* loop over photo file
        for img in photo_file:
            if img:
                #* making a get request to boto3 client
                s3 = boto3.client('s3')
                #* create a new file name to be stored in s3 bucket
                key = uuid.uuid4().hex[:6] + img.name[img.name.rfind('.'):]

                try:
                    #*bucket name
                    bucket = os.environ['S3_BUCKET']
                    #* uploading file using boto3.client method
                    s3.upload_fileobj(img, bucket, key)
                    #* creating photo url from remote aws bucket
                    url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                    #* create a photo instance of the Photo model and assigning it to the created grub
                    Photo.objects.create(url=url, grub=form.instance)
                except Exception as e:
                    print('An error occurred uploading file to S3')
                    print(e)
                    return redirect('home')
            else: 
                print('Need to upload file')
        #* redirect to created grub model instance
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
                except Exception as e:
                    print('An error occurred uploading file to S3')
                    print(e)
                    return redirect('home')
            else: 
                print('Need to upload file')
        return HttpResponseRedirect(self.get_success_url())
    

class GrubDelete(LoginRequiredMixin, DeleteView):
    model = Grub
    success_url = '/grubs/'

class ClaimCreate(LoginRequiredMixin, CreateView):
    model = Claim
    success_url = '/index/'
    fields = '__all__'

    def form_valid(self, form):
        #* assign user to claim from instance
        form.instance.user = self.request.user
        #* save claim with just a user instance
        super().form_valid(form)
        #* return a singular queryset of the updating grub
        grub = Grub.objects.filter(id=self.request.GET.get('id', None))
        #* returns a queryset of a the recently create claim that has no grub instance and belongs to the logged in user
        claim = Claim.objects.filter(grub=None, user=self.request.user)
        #*update the returned claim with the return grub instance
        claim.update(grub=grub[0])
        return redirect('/grubs/')

class PhotoDelete(LoginRequiredMixin, DeleteView):
    model = Photo
    #! use the built-in class method delete 
    def delete(self, request, pk):
        s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
        url = self.request.GET.get("url", None)
        redirect = self.request.GET.get("id", None)
        img_id = self.request.GET.get("img", None)
        #! slice the last 10 char from s3 bucket url string
        img = url[-10:]
        #! make a query fo the photo that matches the photo instace id which comes from hidden form data in template view, passed in through the request
        photo_delete = Photo.objects.get(id=img_id)
        photo_delete.delete()
        #! use the boto3 method to delete from s3 bucket(only made possible if delete_obj action is enable and versioning it disabled in AWS)
        deleted = s3.delete_object(Bucket=os.environ['S3_BUCKET'], Key=img)
        #! use django built in signal and method (first arg) to relay the deleted action of the Photo(second arg) to AWS once completed
        @receiver(post_delete, sender=Photo)
        def delete_image_file(sender, instance, **kwargs):                          
            instance.main_image.delete(False)
        return HttpResponseRedirect(reverse('grubs_detail', kwargs={'pk':redirect}))
