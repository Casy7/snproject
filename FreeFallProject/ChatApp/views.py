from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.files import File
from django.db.models import Q
from FreeFallProject.settings import MEDIA_ROOT, MEDIA_URL
from .models import *
from .forms import *
import datetime
import base64
import json
import re


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
        if len(Profile.objects.filter(user=user)) != 0:

            context['username'] = user.username
            if bool(user.profile.avatar):
                context['avatar'] = user.profile.avatar
            else:
                context['avatar'] = ''
        else:
            user_desc = Profile(user=user, gender='male')
            context['avatar'] = ''
            context['username'] = 'Adminius'
        context['user'] = user
        context['hikes'] = []
        hikes = Hike.objects.filter(
            creator=user).order_by('-creation_datetime')
        if len(hikes) > 10:
            hikes = hikes[:10]
        for hike in hikes:
            context['hikes'].append([hike.name, hike.id])
    else:
        context['username'] = ''
        context['avatar'] = ''
    if args != None:
        for arg in args:
            context[arg] = args[arg]
    # print(context)
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
            request, title='Регистрация', header='Регистрация', error=0)

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
            user_desc = Profile(user=User.objects.get(
                username=form['username']), gender=form['gender'])
            user_desc.save()

            # print(form)
            return HttpResponseRedirect("/login")


        else:
            context = base_context(request, title='Регистрация',
                               header='Регистрация')


            for field_name in form.keys():
                context[field_name] = form[field_name]


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
            request, title='Вход', header='Вход в систему', error=0)
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


class NewHike(View, LoginRequiredMixin):
    def get(self, request):

        context = base_context(
            request, title='Новый поход', header='Новый поход', error=0)
        user_list = []
        for user in User.objects.all():
            if user.last_name != '' and user.first_name != '':
                user_list.append(
                    (user.username, user.username+", "+user.first_name+' '+user.last_name))
            elif user.first_name != '':
                user_list.append(
                    (user.username, user.username+", "+user.first_name))
            elif user.last_name != '':
                user_list.append(
                    (user.username, user.username+", "+user.last_name))
            else:
                user_list.append((user.username, user.username))
        context['user_list'] = user_list
        context['form'] = HikeForm()
        # context['photo_form'] = photo_form
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
        # print(form)

        user = request.user

        if request.user.is_anonymous == False:
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
        

        # Криповый код, считающий количество дней между датами начала и конца похода.
        a = hike.start_date.split('-')
        b = hike.end_date.split('-')
        aa = datetime.date(int(a[0]),int(a[1]),int(a[2]))
        bb = datetime.date(int(b[0]),int(b[1]),int(b[2]))
        days_count = int(str(bb-aa).split()[0])
        # Конец выделеного комментарием крипового кода. Дальше просто криповый код.
        
        for i in range (1, days_count+1):
            day = Day(
                name = "День " + str(i),
                date = aa + datetime.timedelta(i),
            )
            day.save()
            hike.days.add(day)
        hike.save()



        return HttpResponseRedirect("/editor/"+str(hike.id))


class HikeEditor(View, LoginRequiredMixin):
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
                'landmarks': list(Landmark.objects.filter(is_public=True)),
                'description': hike.description,
                'coordinates': hike.coordinates,
            })

            return render(request, "editor.html", context)

        else:
            return HttpResponseRedirect("/login/")

    def post(self, request, id):

        form = request.POST

        #  print(form)
        hike = Hike.objects.get(id=id)
        if form['landmarks'] != '':
            landmark_list = eval(form['landmarks'])
            for lk in landmark_list:
                new_landmark = Landmark(name=lk[1])
                new_landmark.longitude = lk[0][0]
                new_landmark.latitude = lk[0][1]
                new_landmark.description = lk[2]
                if lk[3] == "on":
                    new_landmark.is_public == True
                else:
                    new_landmark.is_public == False
                new_landmark.save()

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
        # hike.creator = user

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

        delete = str(form['cord_del'])
        data = delete.split(',')
        delete = []
        for i in range(len(data)//3):
            delete.append(
                [int(data[i*3]), [float(data[i*3+1]), float(data[i*3+2])]])

        for el in delete:
            coordinates.remove(el)

        hike.coordinates = coordinates
        print(coordinates, delete)
        if 'image' in request.FILES.keys():
            hike.image = request.FILES['image']
        elif 'delete_photo' in form.keys():
            hike.image = None

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
            start_date__gte=datetime.date.today()).order_by('-creation_datetime')

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
                text['creator'] = hike.creator

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
        # print(coordinates)
        hike.save()
        return render(request, "hikes.html", context)


class SetHike(View):
    def get(self, request, id):

        hike = Hike.objects.get(id=id)
        context = base_context(request, title=hike.name, header=hike.name)
        this_hike = {}
        this_hike['current_user'] = request.user
        this_hike['creator'] = hike.creator
        this_hike['name'] = hike.name
        this_hike['id'] = hike.id
        this_hike['start_date'] = hike.start_date
        this_hike['end_date'] = hike.end_date
        this_hike['short_description'] = hike.short_description
        this_hike['description'] = hike.description
        this_hike['coordinates'] = hike.coordinates
        # Сюда вставить все достопримечательности
        this_hike['landmarks'] = list(Landmark.objects.filter(is_public=True))
        # text['image'] = hike.image
        if hike.image.name is not None and hike.image.name != "":
            this_hike['image'] = hike.image
        else:
            this_hike['image'] = ''
        # landmarks = []
        # for landmark in hike.landmarks.all():
        #     landmarks.append(landmark.name)

        # this_hike['landmarks'] = hike.landmarks
        participants = []

        for participant in hike.participants.all():
            participants.append(participant.username)

        this_hike['participants'] = participants
        this_hike['coordinates'] = hike.coordinates
        context['content'] = this_hike

        return render(request, "hike.html", context)

    def post(self, request, id):
        context = base_context(request)
        form = request.POST
        data = form['participate']
        if data == "Yup":
            hike = Hike.objects.get(id=id)
            hike.participants.add(request.user)
        hike.save()
        return HttpResponseRedirect("/hike/"+str(hike.id))


class MyAccount(View):

    def get(self, request):

        user = request.user

        first_name = user.first_name
        last_name = user.last_name
        username = user.username

        if len(Profile.objects.filter(user=user)) == 0:
            profile = Profile(user=user)
        else:
            profile = Profile.objects.get(user=user)

        if first_name != '' and last_name != '':
            full_name = last_name+" "+first_name
        elif first_name != '':
            full_name = first_name
        else:
            full_name = username

        context = base_context(request, title=full_name, header=username)
        context['user'] = user
        context['profile'] = profile
        context['full_name'] = full_name
        context['contacts'] = Contact.objects.filter(user=user)
        context['list_of_alowed_positions'] = ["phone", "telegram", "email"]
        # context['list_of_alowed_visible_conds'] = ["noone","friends","all"]
        return render(request, "my_account.html", context)


class AccountEditor(View):

    def get(self, request):

        user = request.user

        first_name = user.first_name
        last_name = user.last_name
        username = user.username

        if len(Profile.objects.filter(user=user)) == 0:
            profile = Profile(user=user)
        else:
            profile = Profile.objects.get(user=user)

        if first_name != '' and last_name != '':
            full_name = last_name+" "+first_name
        elif first_name != '':
            full_name = first_name
        else:
            full_name = username

        context = base_context(request, title=full_name, header=username)
        context['user'] = user
        context['profile'] = profile
        context['full_name'] = full_name
        context['contacts'] = Contact.objects.filter(user=user)
        context['list_of_alowed_positions'] = ["phone", "telegram", "email"]
        # context['list_of_alowed_visible_conds'] = ["noone","friends","all"]
        return render(request, "account_editor.html", context)

    def post(self, request):
        # TODO валидация этой формы
        form = request.POST
        user = request.user

        if form['first_name'] != '':
            user.first_name = form['first_name']
        user.last_name = form['last_name']
        user.save()

        if len(Profile.objects.filter(user=user)) == 0:
            profile = Profile(user=user)
        else:
            profile = Profile.objects.get(user=user)

        profile.save()

        profile.about = form['about']

        if 'image' in request.FILES.keys():
            profile.avatar = request.FILES['image']
        elif 'delete_photo' in form.keys():
            profile.avatar = None

        profile.request_for_participation = form["request"]
        profile.add_to_participation = form["add_to_ptc"]
        profile.see_hikes = form["can_see_hikes"]

        profile.save()
        # Добавление контактов
        for old_contact in Contact.objects.filter(user=user):
            old_contact.delete()

        contact_number = 0
        for contact in form.keys():
            if 'contact_name_' in contact:
                id = re.findall('\d+', contact)[0]
                if form[contact] != '' and form['contact_value_'+id] != '':
                    new_contact = Contact(
                        user=user, name=form[contact], value=form['contact_value_'+id], visible_for=form['contact_visibility_'+id])
                    new_contact.save()

        context = base_context(request)
        return HttpResponseRedirect('/my_account/')


class DoesUserExist(View):
    def post(self, request):
        req = request
        form = request.POST

        result = {}
        if len(User.objects.filter(username=form['username'])) > 0:
            result['exist'] = 'True'
            result['exist_image'] = False
            user = User.objects.get(username=form['username'])
            if len(Profile.objects.filter(user=user)) and user.profile.avatar.name != '':
                result['exist_image'] = True
                image = user.profile.avatar
                with open(MEDIA_ROOT+image.name, "rb") as img_file:
                    my_string = base64.b64encode(img_file.read()).decode("ASCII") 
                result['image'] = my_string
        else:
            result['exist'] = 'False'
        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )


class IsNewHikeValid(View):
    def post(self, request):
        req = request
        form = HikeForm(request.POST)
        if form.is_valid():
            pass
        result = {}
        if len(User.objects.filter(username=form['username'])) > 0:
            result['exist'] = 'True'
        else:
            result['exist'] = 'False'
        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )
