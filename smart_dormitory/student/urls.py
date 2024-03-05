from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('property/', views.property, name='property'),
    path('properties/<int:pk>/', views.property_detail, name='property-detail'),
    path('about/', views.about, name='about'),
    path('404/', views.page_not_found, name='404'),
    path('contact/', views.contact, name='contact'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('profile-form/', views.profileForm, name='profileForm'),
    path('user-profile/<str:pk>', views.userProfile, name='user-profile'),
    path('update-profile/<str:pk>', views.updateProfile, name='update-profile'),
]
