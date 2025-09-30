from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("HI this is the front page of the notes app")



def notes(request):
    return render(request,'notes.html')

def note_add(request):
    return HttpResponse("soon to be notes_add page")

