from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, logout, login

# Create your views here.
from django.http import HttpResponse


class Index(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    template_name = 'bankSystem/index_page.html'

def log_in(request):		
    if request.user.is_authenticated:
        return redirect('bankSystem:index', )
    # form = my_forms.UserForm
    return render (request, 'bankSystem/login.html')


def log_out(request):
    logout(request)
    return redirect('bankSystem:login')


def check_login(request):
    nickname = request.POST['nickname']
    password = request.POST['password']
    user = authenticate(username=nickname, password=password)
    if user:
        login(request, user)
        return redirect('bankSystem:index', )
    else:
        return HttpResponse("Ошибка входа")