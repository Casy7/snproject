from django.views.generic import View, TemplateView
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import *
# Create your views here.


def home(request):
    context = {

    }
    return render(request, "main.html", context)

class Registration(View):
    def get(self, request):
        context = {

        }

        return render(request, "registration.html", context)
    def post(self, request):
        context = {}
        form = request.POST
        user_props = {}
        for prop in form:
            if prop not in ('csrfmiddlewaretoken','username') and form[prop]!="":
                user_props[prop] = form[prop]
        # print(user_props)
        StandartUser.objects.create_user(username = form['username'],**user_props)
        # print(form)
        return HttpResponseRedirect("/login")




class UserLogin(View):
    # permission_required = ('posts.can_view', 'login.can_view')
    # template_name = 'create_post.html'
    # permission_denied_message = "Sorry. Access denied"
    # raise_exception = True
    def __init__(self):
        self.error = 0
    # form_class = LoginUser

    def get(self, request):
        context = {

        }
        # context['form'] = self.form_class()
        return render(request, "login.html", context)

    def post(self, request):
        context = {}
        form = request.POST
        # validation = UserForm(request.POST)
        if True: # validation.is_valid():
            # print(form)
            username = form['username']
            password = form['password']

            # new_post.author = Author.objects.get(id = request.POST.author)
            # new_post.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    context['name'] = username
                    return HttpResponseRedirect("/")
            elif authenticate(username=username, password=password) is not None:
                user = authenticate(email=username, password=password)
                if user.is_active:
                    login(request, user)
                    context['name'] = username
                    return HttpResponseRedirect("/")                
            else:
                self.error = 1
                # return Posts.get(self,request)
                return HttpResponse("Authentication error. Password or username is invalid.")
        else:
            return HttpResponse("Data isn't valid")

