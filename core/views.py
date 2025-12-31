from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import views as auth_views
from .forms import SignUpForm

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class UserLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    # On successful login, redirect to the dashboard home page.
    next_page = reverse_lazy('dashboard:home')

class UserLogoutView(auth_views.LogoutView):
    # On successful logout, redirect to the dashboard home page.
    next_page = reverse_lazy('dashboard:home')
