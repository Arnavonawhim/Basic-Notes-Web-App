from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

def login_page(request):
    email=request.POST.get("email")
    password=request.POST.get("password")
    
    if not User.objects.filter(email=email).exists():
        messages.error(request,"Email Is not registered")
        return render(request,'login.html')
    else:
        person=User.objects.get(email=email)

    person = authenticate(request, username=person.username, password=password)
    if person is not None:
        login(request,person)
        return redirect('notes')
    else:
        messages.error(request, "Invalid email or password") 
        return render(request, 'login.html')
    


def register(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    password=request.POST.get('password')

    if not name or not email or not password:
        messages.error(request,"Enter All The Details")
        return render(request,'Register.html')
    
    if User.objects.filter(username=email).exists():
        messages.error(request,"User Already Registered Go To Login Page")
        return render(request,'Register.html')
    
    person=User.objects.create_user(username=email,email=email,password=password,first_name=name)
    return render(request,'Register.html')
    #return redirect notes

def logout_person(request):
    logout(request)
    return redirect('login_page')