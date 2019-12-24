from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.files import File
from django.db.models import Q
from .models import *
from .forms import *
import datetime


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
        context['user'] = user
        context['hikes'] = []
        hikes = Hike.objects.filter(creator=user).order_by('creation_datetime')
        if len(hikes) > 10:
            hikes = hikes[:10]
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


def participants_new_format(participants):
    participants = str(participants)
    participants = participants.split(sep=',')

    pt_list = []
    for pt in participants:
        if pt != '':

            user = User.objects.filter(username=pt)
            if list(user) != []:
                pt_list.append(user[0])
    return pt_list


def parts_revert_format(participants):
    text_format = ""
    for pt in participants:
        text_format += '@'+pt.username+'\t'
    return text_format


class HomePage(View):
    def get(self, request):
        context = base_context(request, title='Home', header='Lorem Ipsum')
        return render(request, "main.html", context)


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


class AddLandmark(View):
    def post(self, request):
        context = request.POST


class NewHike(View):
    def get(self, request):
        photo_form = PhotoForm()
        context = base_context(
            request, title='New Hike', header='Новый поход', error=0)

        context['form'] = HikeForm()
        context['photo_form'] = photo_form
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

        if user is not None or request.user.is_anonymous == False:
            # if user.is_active:
            #     login(request, user)
            #     context['name'] = username
            #     return HttpResponseRedirect("/")
            # else:
            context['name'] = request.user.username
            user = request.user
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
        if 'image' in request.FILES.keys():
            hike.image = request.FILES['image']
        participants = participants_new_format(form['participants'])
        for pt in participants:
            hike.participants.add(pt)
        hike.save()

        return HttpResponseRedirect("/editor/"+str(hike.id))


class HikeEditor(View):
    def get(self, request, id):

        hike = Hike.objects.get(id=id)

        context = base_context(
            request, title='Track', header='Изменение похода: '+hike.name)

        if hike.image.name is not None:
            context['image'] = hike.image
        else:
            context['image'] = ''

        if context['username'] != '' and request.user == hike.creator:
            participants = []
            for user in hike.participants.all():
                participants.append(user.username)
            context.update({
                'name': hike.name,
                'short_description': hike.short_description,
                'start_date': str(hike.start_date),
                'end_date': str(hike.end_date),
                'difficulty': hike.difficulty,
                'type_of_hike': hike.type_of_hike,

                'participants': participants,
                # '':hike.,
                'description': hike.description,
                'coordinates': hike.coordinates,
            })

            return render(request, "editor.html", context)

        else:
            return HttpResponseRedirect("/login/")

    def post(self, request, id):
        context = base_context(request)
        form = request.POST

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

        hike = Hike.objects.get(id=id)
        hike.name = form['name']

        coordinates = []
        i = 0
        while True:
            if form.get("start_day"+str(i)) != None:
                tpl = form["start_day" +
                           str(i)].replace("(", "").replace(")", "").split(";")

                coordinates.append(tpl)
                tpl = form["end_day" +
                           str(i)].replace("(", "").replace(")", "").split(";")

                coordinates.append(tpl)
                i += 1

            else:
                break
        hike.creator = user

        hike.short_description = form['short_description']
        hike.description = form['description']
        hike.start_date = form['start']
        hike.end_date = form['end']
        hike.difficulty = form['difficulty']
        hike.type_of_hike = form['type']

        coordinates = str(form['coordinates'])
        data = coordinates.split(',')
        coordinates = []
        for i in range(len(data)//3):
            coordinates.append(
                [int(data[i*3]), [float(data[i*3+1]), float(data[i*3+2])]])
                
        hike.coordinates = coordinates
        if 'image' in request.FILES.keys():
            hike.image = request.FILES['image']

        hike.save()
        # participants = participants_format(form['participants'])
        participants = participants_new_format(form['participants'])
        already_in_hike = hike.participants.all()
        for pt in participants:
            if pt not in already_in_hike:
                hike.participants.add(pt)
        hike.save()

        return HttpResponseRedirect("/hike/"+str(hike.id))


class Logout (View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class AllHikes(View):

    def get(self, request):
        context = base_context(request, title='Hikes')

        context['hike'] = []

        hikes = Hike.objects.filter(
            start_date__gte=datetime.date.today()).order_by('creation_datetime')

        # Возвращает список походов, начинающихся не ранее чем сегодня,
        # отсортированный по давности их создания.

        hike_stack = []
        stack_index = 0
        index = 0
        while index < len(hikes):

            stack_index = 0
            hike_row = []
            while stack_index < 4 and index < len(hikes):
                hike = hikes[index]

                text = {}
                text['link'] = '/hike/' + str(hike.id)
                text['name'] = hike.name
                text['start_date'] = hike.start_date

                if hike.image.name is not None:
                    text['image'] = hike.image
                else:
                    text['image'] = ''
                text['end_date'] = hike.end_date
                text['short_description'] = hike.short_description

                if len(text['short_description']) > 200:
                    text['short_description'] = text['short_description'][0:198]+'...'

                hike_row.append(text)
                stack_index += 1
                index += 1

            context['hike'].append(hike_row)

        return render(request, "hikes.html", context)


class MapOfHike(View):

    def get(self, request, id):

        context = base_context(request, title='Map')
        text = {}
        hike = Hike.objects.get(id=id)
        text['coordinates'] = hike.coordinates
        context['content'] = text
        return render(request, "map.html", context)


class CreateMap(View):

    def get(self, request, id):

        context = base_context(request, title='Map')
        text = {}
        hike = Hike.objects.get(id=id)
        text['coordinates'] = hike.coordinates
        context['content'] = text
        return render(request, "create_map.html", context)

    def post(self, request, id):
        context = base_context(request)
        form = request.POST

        data = form['coordinates'].split(',')
        coordinates = []
        for i in range(len(data)//3):
            coordinates.append(
                [int(data[i*3]), [float(data[i*3+1]), float(data[i*3+2])]])

        hike = Hike.objects.get(id=id)
        hike.coordinates = coordinates
        print(coordinates)
        hike.save()
        return render(request, "hikes.html", context)


class SetHike(View):
    def get(self, request, id):

        hike = Hike.objects.get(id=id)
        context = base_context(request, title=hike.name, header=hike.name)
        text = {}
        text['creator'] = hike.creator
        text['name'] = hike.name
        text['id'] = hike.id
        text['start_date'] = hike.start_date
        text['end_date'] = hike.end_date
        text['short_description'] = hike.short_description
        text['description'] = hike.description
        text['coordinates'] = hike.coordinates
        text['image'] = hike.image
        text['link'] = '/map/' + str(hike.id)
        if hike.image.name is not None and hike.image.name!="":
            text['image'] = hike.image
        else:
            text['image'] = ''
        landmarks = []
        for landmark in hike.landmarks.all():
            landmarks.append(landmark.name)

        text['landmarks'] = hike.landmarks
        participants = []

        for participant in hike.participants.all():
            participants.append(participant.username)

        text['participants'] = participants
        text['coordinates'] = hike.coordinates
        context['content'] = text

        return render(request, "hike.html", context)
