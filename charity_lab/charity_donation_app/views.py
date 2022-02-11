from IPython.lib.pretty import pprint
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView

from .forms import UserRegisterForm, UserLoginForm
from .models import Category, Institution, Donation


User = get_user_model()

class LandingPage(View):
    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all()
        bags = 0
        for donation in donations:
            bags = bags + donation.quantity
        institutions = Institution.objects.count()
        foundations = Institution.objects.filter(type=0)
        organizations = Institution.objects.filter(type=1)
        local_orgs = Institution.objects.filter(type=2)
        if self.request.user.is_authenticated:
            user_name =self.request.user.first_name
        else:
            user_name = None
        ctx = {
            'bags': bags,
            'institutions': institutions,
            'foundations': foundations,
            'organizations': organizations,
            "locals": local_orgs,
            "user_name": user_name,
        }
        return render(request, template_name='index.html', context=ctx)


class AddDonation(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        institutions_json = serializers.serialize('json', Institution.objects.all())
        if self.request.user.is_authenticated:
            user_name =self.request.user.first_name
        else:
            user_name = None
        ctx = {
            'categories': categories,
            'institutions': institutions_json,
            'user_name': user_name,
        }
        return render(request, template_name='form.html', context=ctx)

    def post(self, request, *args, **kwargs):
        return render(request, template_name='form.html')


class SuccessPage(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            user_name =self.request.user.first_name
        else:
            user_name = None
        ctx = {
            'user_name': user_name,
        }
        return render(request, template_name='form-confirmation.html', context=ctx)


class Login(View):
    """
     Logs the user in. If user with the given credentials is not found, redirects to registration form.
        If user is found, logs user in and redirects to main page.
    """

    def get(self, request, *args, **kwargs):
        ctx = {
            'form': UserLoginForm(),
        }
        return render(request, template_name='login.html', context=ctx)

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            email = clean_data['email']
            password = clean_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                return redirect('register')


class Register(View):
    """
    Saves a user with given name, surname, email and password to the database. After successful save
        redirects to login page.
    """

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            user_name =self.request.user.first_name
        else:
            user_name = None
        ctx = {
            'form': UserRegisterForm(),
            'user_name': user_name
        }
        return render(request, template_name='register.html', context=ctx)

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            User.objects.create_user(
                first_name=clean_data['name'],
                last_name=clean_data['surname'],
                email=clean_data['email'],
                password=clean_data['password'],

            )
        else:
            ctx = {
                'form': form,
            }
            return render(request, template_name='register.html', context=ctx)
        return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('main')


class UserDetail(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_donations = Donation.objects.filter(user=user)
        if self.request.user.is_authenticated:
            user_name =self.request.user.first_name
        else:
            user_name = None
        ctx = {
            'user': user,
            'user_name': user_name,
            'donations': user_donations,
        }
        return render(request, template_name='user-detail.html', context=ctx)
