from django.contrib.auth.views import LogoutView
from django.urls import path
from social_auth import views

urlpatterns = [
    path('login/', views.index, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
