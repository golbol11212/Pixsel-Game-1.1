from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'game/home.html')

def about(request):
    return HttpResponse("<h1>About Pixsgame</h1><p>This is a Django website for pixel games!</p>")
