from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def home(request):
    return HttpResponse('aaa')


def privacy(request):
    return render(request, 'places_remember/privacy-policy.html')
