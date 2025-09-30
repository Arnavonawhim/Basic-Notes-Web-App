from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("HI this is the front page of the notes app")

def home(request):
    return render(request,'login.html')

def register(request):
    return render(request,'Register.html')