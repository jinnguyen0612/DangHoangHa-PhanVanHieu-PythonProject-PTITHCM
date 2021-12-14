import string
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from passlib.hash import django_pbkdf2_sha256

# Create your views here.
def lower(s):
    lower = any(c.islower() for c in s)
    return lower

# private function to check password must use Atleast 1 upper case character
def upper(s):
    upper = any(c.isupper() for c in s)
    return upper

# private function to check password must use Atleast 1 number
def digit(s):
    digit = any(c.isdigit() for c in s)
    return digit

def whiteSpace(s):
    white_space = any(c.isspace() for c in s)
    return white_space


class Register(View):

    def  get(self, request):

        return render(request, 'user/register.html')
    def post(self, request):
        username = request.POST.get('inputUsername')
        password = request.POST.get('inputPassword')
        confirm_password = request.POST.get('reInputPassword')

        if whiteSpace(username):
            return render(request,'user/register.html',{"error":"Do not contain spaces in usernames"})

        if len(password)<8:
            return render(request,'user/register.html',{"error":"Password should Atleast have 8 character"})
        elif not lower(password):
            return render(request, 'user/register.html', {"error": "You didn't use LOWER case letter"})
        elif not upper(password):
            return render(request, 'user/register.html', {"error": "You didn't user UPPER case letter"})
        elif not digit(password):
            return render(request, 'user/register.html', {"error": "You didn't use DIGIT"})
        elif password!=confirm_password:
            return render(request,'user/register.html',{"error":"Password and confirmation do not match"})
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username,
                                            email='',
                                            password=password,is_staff=True)
            user.user_permissions.set([25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40])

            return redirect("/user/Login/")

        return render(request, 'user/register.html', {"error": "Tai khoan da ton tai"})


class LoginClass(View):
    def get(self,request):
        return render(request,'user/login.html')

    def post(self,request):
        username=request.POST.get('username')
        password = request.POST.get('password')
        my_user = authenticate(username=username, password=password)
        if my_user is None:
            return render(request,'user/login.html',{"error":'Login failed! Username does not exist or password is wrong'})
        login(request,my_user)
        return redirect("/")

class ForgotPassword(View):
    def get(self, request):
        return render(request,'user/forgot_password.html')

    def post(self,request):
        username = request.POST.get('inputUsername')
        password = request.POST.get('inputPassword')
        confirm_password = request.POST.get('reInputPassword')

        if whiteSpace(username):
            return render(request, 'user/forgot_password.html', {"error": "Do not contain spaces in usernames"})

        try:
            user = User.objects.get(username=username)

            if len(password) < 8:
                return render(request, 'user/forgot_password.html',
                              {"error": "Password should Atleast have 8 character"})
            elif not lower(password):
                return render(request, 'user/forgot_password.html', {"error": "You didn't use LOWER case letter"})
            elif not upper(password):
                return render(request, 'user/forgot_password.html', {"error": "You didn't user UPPER case letter"})
            elif not digit(password):
                return render(request, 'user/forgot_password.html', {"error": "You didn't use DIGIT"})
            elif password != confirm_password:
                return render(request, 'user/forgot_password.html', {"error": "Password and confirmation do not match"})

            rounds = user.password.split('$')[1]
            salt = user.password.split('$')[2]
            password_new_hash = django_pbkdf2_sha256.hash(password, rounds=rounds, salt=salt)
            User.objects.filter(pk=user.pk).update(password=password_new_hash)
            return redirect('/user/Login/')
        except User.DoesNotExist:
            return render(request, 'user/forgot_password.html', {"error": "Account does not exist"})


def logoutPage(request):
    logout(request)
    return redirect('/')

class UpdateProfile(LoginRequiredMixin, View):
    login_url = '/user/Login/'
    def get(self,request):
        return render(request, 'user/update_profile.html')
    def post(self, request):
        user_pk = request.user.pk
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('Email')
        if whiteSpace(username):
            return render(request,'user/update_profile.html',{"error":"Do not contain spaces in usernames"})
        User.objects.filter(pk=user_pk).update(username=username, first_name=first_name, last_name= last_name, email= email )
        return redirect('/')

class ChangePassword(LoginRequiredMixin, View):
    login_url = '/user/Login/'
    def get(self,request):
        return render(request, 'user/change_password.html')
    def post(self, request):
        user = request.user
        password_user =  user.password
        password_old = request.POST.get('password_old')
        password_new = request.POST.get('password_new')
        password_cofirm = request.POST.get('password_cofirm')
        if django_pbkdf2_sha256.verify(password_old, password_user) == False:
            return render(request, 'user/change_password.html', {'error': "Old password entered is not correct"})
        if len(password_new)<8:
            return render(request,'user/change_password.html',{"error":"Password should Atleast have 8 character"})
        elif not lower(password_new):
            return render(request, 'user/change_password.html', {"error": "You didn't use LOWER case letter"})
        elif not upper(password_new):
            return render(request, 'user/change_password.html', {"error": "You didn't user UPPER case letter"})
        elif not digit(password_new):
            return render(request, 'user/change_password.html', {"error": "You didn't use DIGIT"})
        elif password_new!=password_cofirm:
            return render(request,'user/change_password.html',{"error":"Password and confirmation do not match"})

        rounds = password_user.split('$')[1]
        salt = password_user.split('$')[2]
        password_new_hash=django_pbkdf2_sha256.hash(password_new, rounds=rounds, salt=salt)
        User.objects.filter(pk=user.pk).update(password= password_new_hash)
        my_user = authenticate(username=user.username, password=password_new)
        login(request, my_user)
        return redirect("/")

def randomPassword(request):
    chars_fixed = string.ascii_letters + string.digits
    min_size_pass = 8
    max_size_pass = 15
    password = "".join(random.choice(chars_fixed) for x in range(random.randint(min_size_pass, max_size_pass)))
    return render(request, 'user/register.html',{'password_random':password})