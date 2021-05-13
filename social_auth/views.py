from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy


def login(request):
    if not request.user.is_authenticated:
        return render(request, 'social_auth/login.html')
    else:
        return HttpResponseRedirect(reverse_lazy('home'))
