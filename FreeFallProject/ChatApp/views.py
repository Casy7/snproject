from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import *


def new_format(coordinates):
    coordinates = list(coordinates.split(";"))
    new_coords = []
    for coord in coordinates:
        if coord != "":
            new_coords.append(
                (coord[3:coord.find("lat=")], coord[coord.find("lat=")+4:]))
    return new_coords


def base_context(request, **args):
    context = {}
    user = request.user

    context['title'] = 'none'
    context['header'] = 'none'
    context['error'] = 0
    if user.is_anonymous != True:
        context['username'] = user.username

        context['hikes'] = []
        hikes = Hike.objects.filter(creator=user)

        for hike in hikes:
            context['hikes'].append([hike.name, hike.id])
    else:
        context['username'] = ''
    if args != None:
        for arg in args:
            context[arg] = args[arg]
    return context


def participants_format(participants):
    participants = str(participants)
    participants = participants.replace('\t', '').replace(' ', '')
    participants = participants.split(sep='@')

    pt_list = []
    for pt in participants:
        if pt != '':

            user = User.objects.filter(username=pt)
            if list(user) != []:
                pt_list.append(user[0])
    return pt_list


class HomePage(View):
    def get(self, request):
        context = base_context(request, title='Home', header='Lorem Ipsum')
        return render(request, "main.html", context)


class HomePage_test(View):
    def get(self, request):
        context = base_context(request, title='Home', header='Lorem Ipsum')
        return render(request, "test_base.html", context)


class Registration(View):
    def get(self, request):

        context = base_context(
            request, title='Registration', header='Registration', error=0)

        return render(request, "registration.html", context)

    def post(self, request):
        context = {}
        form = request.POST
        user_props = {}
        username = form['username']
        password = form['password']

        # new_post.author = Author.objects.get(id = request.POST.author)
        # new_post.save()
        user = User.objects.filter(username=username)
        if list(user) == []:
            for prop in form:
                if prop not in ('csrfmiddlewaretoken', 'username', 'gender') and form[prop] != '':
                    user_props[prop] = form[prop]
            # print(user_props)
            User.objects.create_user(
                username=form['username'], **user_props)
            user_desc = Description(user=User.objects.get(
                username=form['username']), gender=form['gender'])
            user_desc.save()

            # print(form)
            return HttpResponseRedirect("/login")
        else:
            context = base_context(request)
            context['error'] = 1
            return render(request, "registration.html", context)


class UserLogin(View):
    # permission_required = ('posts.can_view', 'login.can_view')
    # template_name = 'create_post.html'
    # permission_denied_message = "Sorry. Access denied"
    # raise_exception = True
    def __init__(self):
        self.error = 0
    # form_class = LoginUser

    def get(self, request):
        context = base_context(
            request, title='Login', header='Login', error=0)
        context['error'] = 0
        # context['form'] = self.form_class()
        return render(request, "login.html", context)

    def post(self, request):
        context = {}
        form = request.POST
        # validation = UserForm(request.POST)
        if True:  # validation.is_valid():
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

            else:
                context = base_context(request)
                context['error'] = 1
                # return Posts.get(self,request)
                return render(request, "login.html", context)
        else:
            return HttpResponse("Data isn't valid")


class NewHike(View):
    def get(self, request):
        context = base_context(
            request, title='New Hike', header='Новый поход', error=0)
        if context['username'] != '':
            return render(request, "new_hike.html", context)
        else:
            context['error'] = 2
        # context['form'] = self.form_class()
            return render(request, "login.html", context)

    def post(self, request):
        context = base_context(request)
        form = request.POST

        user_props = {}
        print(form)

        username = request.user.username
        password = request.user.password

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                context['name'] = username
                return HttpResponseRedirect("/")
        else:
            user = User.objects.get(username='admin')

        hike = Hike(
            name=form['name'],
            creator=user,
            short_description=form['short_description'],
            # description=form['description'],
            start_date=form['start'],
            end_date=form['end'],
            difficulty=form['difficulty'],
            type_of_hike=form['type'],
            # coordinates=new_format(form['coordinates'])
        )
        hike.save()
        participants = participants_format(form['participants'])
        for pt in participants:
            hike.participants.add(pt)
        hike.save()

        return HttpResponseRedirect("/map/"+str(hike.id))


class Logout (View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class AllHikes(View):

    def get(self, request):
        context = base_context(request, title='Hikes')


        context['hike'] = []
        hikes = Hike.objects.all()
        hike_stack = []
        stack_index = 0
        index = 0
        while index < len(hikes):
            stack_index = 0
            hike_row = []
            while stack_index < 4 and index<len(hikes):
                hike = hikes[index]

                text = {}
                text['link'] = '/hike/' + str(hike.id)
                text['name'] = hike.name
                text['start_date'] = hike.start_date
                text['end_date'] = hike.end_date
                text['short_description'] = hike.short_description
                if len(text['short_description'])>200:
                    text['short_description'] = text['short_description'][0:198]+'...'
                hike_row.append(text)
                stack_index += 1
                index += 1

            context['hike'].append(hike_row)

        return render(request, "hikes.html", context)


class MapOfHike(View):
    def get(self, request, id):
        context = base_context(
            request, title='Track', header='Создание маршрута похода')
        hike = Hike.objects.get(id=id)
        context['name'] = hike.name
        return render(request, "map.html", context)

    def post(self, request, id):

        form = context.POST


class SetHike(View):
    def get(self, request, id):

        hike = Hike.objects.get(id=id)
        context = base_context(request, title=hike.name)
        text = {}
        text['name'] = hike.name
        text['start_date'] = hike.start_date
        text['end_date'] = hike.end_date
        text['description'] = hike.description
        landmarks = []
        for landmark in hike.landmarks.all():
            landmarks.append(landmark.name)
        text['landmarks'] = hike.landmarks
        participants = []
        for participant in hike.participants.all():
            participants.append(participant.username)
        text['participants'] = participants
        context['content'] = text
        return render(request, "hike.html", context)
