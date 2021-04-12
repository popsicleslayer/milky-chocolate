from django.shortcuts import render
from django.views import View


class LandingPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='index.html')


class AddDonation(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='form.html')


class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='login.html')


class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='register.html')
