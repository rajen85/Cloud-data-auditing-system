from django.urls import path
from .views import UserListCreateAPIView, UserDetailAPIView, UserCreateAPIView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('userregister/', views.userregister, name='userregister'),
    path('userlogin/', views.userlogin, name='userlogin'),

    # API routes
    path('api/users/', UserListCreateAPIView.as_view(), name='user-list'),
    path('api/users/register/', UserCreateAPIView.as_view(), name='user-register'),
    path('api/users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('uploadfiles/', views.uploadfiles, name='uploadfiles'),
    path('viewfiles/', views.viewfiles, name='viewfiles'),
    path('myfiles/', views.myfiles, name='myfiles'),
    path('sendauditrequest/<int:id>/', views.sendauditrequest, name='sendauditrequest'),
    path('cloudlogin/', views.cloudlogin, name='cloudlogin'),
    path('ptpclogin/', views.ptpclogin, name='ptpclogin'),
    path('viewauditrequest/', views.viewauditrequest, name='viewauditrequest'),
    path('sendchallange/<int:id>/', views.sendchallange, name='sendchallange'),
    path('viewchallanges/', views.viewchallanges, name='viewchallanges'),
    path('sendproof/<int:id>/', views.sendproof, name='sendproof'),
    path('cloudresponses/', views.cloudresponses, name='cloudresponses'),
    path('verifyproof/<int:id>/', views.verifyproof, name='verifyproof'),
    path('sendfilerequest/<int:id>/', views.sendfilerequest, name='sendfilerequest'),
    path('viewfilerequests/', views.viewfilerequests, name='viewfilerequests'),
    path('decryptfile/<int:id>/', views.decryptfile, name='decryptfile'),
    path('viewresponses/', views.viewresponses, name='viewresponses'),
    path('downloadfile/<int:id>/', views.downloadfile, name='downloadfile'),


]
