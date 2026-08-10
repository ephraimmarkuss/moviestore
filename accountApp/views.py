from django.shortcuts import render , redirect
from django.contrib.auth import login as auth_login, authenticate , logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm , CustomerErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')


def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accountApp/login.html',{'template_data':template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password'])
        if user is None :
            template_data['error']='The username or passworf is incorrect.'
            return render(request,'accountApp/login.html',{'template_data ': template_data})
        else:
            auth_login(request , user)
            return redirect('home')



def signup(request):
    template_data ={}
    template_data['title'] = 'sign up'

    if request.method == 'GET':
        template_data['form']= CustomUserCreationForm()
        return render(request, 'accountApp/signup.html',{'template_data':template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST,error_class =CustomerErrorList)
        if form.is_valid():
            form.save()
            return redirect ('login')
        else:
            template_data['form']= form
            return render(request, 'accountApp/signup.html',{'template_data':template_data})


@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accountApp/orders.html',{'template_data': template_data})
        