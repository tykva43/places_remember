from django.urls import path

from social_auth import views

urlpatterns = [
    path('', views.index, name='login'),
]
