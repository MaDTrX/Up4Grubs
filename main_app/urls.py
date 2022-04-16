from django.urls import path
from . import views
from .views import GrubList, GrubCreate, GrubDetail, GrubDelete, GrubUpdate

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('grubs/',GrubList.as_view(), name='index'),
    path('grubs/detail/<int:pk>/',GrubDetail.as_view(), name='grubs_detail'),
    path('grubs/create/',GrubCreate.as_view(), name='grubs_create'),
    path('grubs/update/<int:pk>/',GrubUpdate.as_view(), name='grubs_update'),
    path('grubs/delete/<int:pk>/',GrubDelete.as_view(), name='grubs_delete')
    #checkout path
]