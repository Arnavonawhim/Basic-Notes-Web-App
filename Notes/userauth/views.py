from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User

def home(request):
    return render(request,'login.html')

def register(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    password=request.POST.get('password')

    if not name or not email or not password:
        messages.error(request,"Enter All The Details")
        return render(request,'Register.html')
    
    if User.Objects.filter(username=email).exists():
        messages.error(request,"User Already Registered Go To Login Page")
        return render(request,'register.html')
    
    person=User.objects.create_user(username=name,email=email,password=password,first_name=name)
    #login()

    #return redirect notes

