from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import MemoForm
from .models import Memo


@login_required
def home(request):
    memories = Memo.objects.filter(user_id=request.user.id)
    return render(request, 'places_remember/home.html', {'memories': memories})


def privacy(request):
    return render(request, 'places_remember/privacy-policy.html')


@login_required
def add_memo(request):
    if request.method == 'GET':
        form = MemoForm()
        return render(request, 'places_remember/add_memo.html', {'form': form})
    elif request.method == 'POST':
        form = MemoForm(request.POST)
        new_memo = form.save(commit=False)
        new_memo.user_id = request.user.id
        new_memo.save()
        return HttpResponseRedirect(reverse('home'))