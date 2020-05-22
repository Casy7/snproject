from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.files import File
from django.db.models import Q
from FreeFallProject.settings import MEDIA_ROOT, MEDIA_URL
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from .models import *
from .forms import *
from datetime import date, timedelta
import base64
import json
import re

import io
from django.core.files import File
from PIL import Image

from FreeFallApp.views_functions import *
from FreeFallApp.views_ajax import *
from FreeFallApp.views_editor import *


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

            user = authenticate(username=username, password=password)
            login(request, user)

            # print(form)
            return HttpResponseRedirect("/account_editor/")

        else:
            context = base_context(request, title='Регистрация',
                                   header='Регистрация')

            for field_name in form.keys():
                context[field_name] = form[field_name]

            context['error'] = 1
            return render(request, "registration.html", context)


class UserLogin(View):

    def __init__(self):
        self.error = 0

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
            request, title='Создать поход', header='Создать поход', error=0)
        user_list = []


        for user in User.objects.all().exclude(username = request.user.username):
            user_list.append((user.username, user.username+', '+full_name(user)))


        context['user_list'] = user_list
        context['form'] = HikeForm()
        


        if context['username'] != '':
            return render(request, "new_hike.html", context)
        else:
            context['error'] = 2

            return render(request, "login.html", context)

    def post(self, request):
        context = base_context(request)
        form = request.POST

        user_props = {}
        # print(form)

        user = request.user

        if request.user.is_anonymous == False:
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
            join_to_group=form['can_users_join'],
            limit_of_members=form['limit_of_members']
            # coordinates=new_format(form['coordinates'])
        )
        
        hike.save()
        hike.participants.add(user)


        if 'image' in request.FILES.keys():
            # hike.image = request.FILES['image']
            hike.save()

            (crop_x, crop_y, crop_width, crop_height) = map(float, form['resize_coordinates'].split(' '))
            image = Image.open(request.FILES['image'])
            cropped_image = image.crop((crop_x, crop_y, crop_width+crop_x, crop_height+crop_y))
            thumb_io = io.BytesIO()
            cropped_image.save(thumb_io, image.format, quality=60)

            hike.image.save(image.filename, ContentFile(thumb_io.getvalue()), save = False)
            hike.save()

        
        participants = participants_new_format(form['participants'])
        for pt in participants:
            if pt != user:
                nt = Notification(user=pt, type_of_notification='invite_to_hike')
                nt.from_user = user
                nt.hike=hike
                nt.save()


            # hike.participants.add(pt)
        hike.save()

        # Криповый код, считающий количество дней между датами начала и конца похода.
        a = hike.start_date.split('-')
        b = hike.end_date.split('-')

        if a == b:

            day = Day(
                    hike=hike,
                    name="День 1",
                    date=date(int(a[0]), int(a[1]), int(a[2])),
                )
            day.save()

        else:

            aa = date(int(a[0]), int(a[1]), int(a[2]))
            bb = date(int(b[0]), int(b[1]), int(b[2]))
            days_count = int(str(bb-aa).split()[0]) + 1
        # Конец выделеного комментарием крипового кода. Дальше просто криповый код.

            for i in range(1, days_count+1):
                day = Day(
                    hike=hike,
                    name="День " + str(i),
                    date=aa + timedelta(days=i-1),
                )
                day.save()

        hike.save()

        return HttpResponseRedirect("/editor/"+str(hike.id))


class Logout (View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class AllHikes(View):

    def get(self, request):
        context = base_context(request, title='Hikes')

        context['hike'] = []

        hikes = Hike.objects.filter(
            start_date__gte=date.today()).order_by('-creation_datetime')

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
                months = ['января', 'февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']
                text['link'] = '/hike/' + str(hike.id)
                if hike.difficulty != "none":
                    text['difficulty'] = hike.difficulty
                else:
                    text['difficulty'] = "Без категории"
                text['type_of_hike'] = hike.type_of_hike
                text['name'] = hike.name
                text['rus_date'] = beauty_date_interval(hike.start_date, hike.end_date, True)
                # text['rus_date'] = str(hike.start_date.day)+' '+months[hike.start_date.month-1]+' - '+str(hike.end_date.day)+' '+months[hike.end_date.month-1]
                text['start_date'] = hike.start_date
                text['creator'] = hike.creator

                if hike.image.name is not None:
                    text['image'] = hike.image
                else:
                    text['image'] = ''
                text['end_date'] = hike.end_date
                text['short_description'] = hike.short_description

                if len(text['short_description']) > 250:
                    text['short_description'] = text['short_description'][0:248]

                hike_row.append(text)
                stack_index += 1
                index += 1

            context['hike'].append(hike_row)

        return render(request, "hikes.html", context)



class Posts(View):

    def get(self, request):
        context = base_context(request, title='Posts')

        context['posts'] = []

        posts = Post.objects.all()

        all_posts = []

        months = ['января', 'февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']

        for post in posts:
            ct = {}
            ct['content'] = post.content
            ct['author'] = post.post_author
            ct['author_fullname'] = full_name(post.post_author)
            ct['author_username'] = post.post_author.username

            ct['avatar'] = ''
            if post.post_author.profile.avatar.name != '':
                ct['avatar'] = post.post_author.profile.avatar.url

            published_time = post.creation_datetime.strftime('%H:%M, %d ')+months[post.creation_datetime.month-1]
            ct['time_published'] = published_time
            all_posts.insert(0, ct)
        context['all_posts'] = all_posts



        return render(request, "posts.html", context)



class MapOfHike(View):

    def get(self, request, id):

        context = base_context(request, title='Map')
        text = {}
        hike = Hike.objects.get(id=id)
        text['coordinates'] = hike.coordinates
        context['content'] = text
        return render(request, "map.html", context)



class Discussion(View):

    def get(self, request, id):

        hike = Hike.objects.get(id=id)
        context = base_context(
            request, title='Track', header='Обсуждение похода: '+hike.name)

        all_messages = []

        for message in Message.objects.filter(hike=hike):

            current_message = {}
            
            current_message['author'] = message.author
            current_message['text'] = message.text
            current_message['creation_datetime'] = message.creation_datetime

            all_messages.append(current_message)
        
        context['content'] = all_messages

        return render(request, "discussion.html", context)
    
    def post(self, request, id):

        form = request.POST
        user = request.user
        hike = Hike.objects.get(id=id)

        text = form['text'].replace("\r\n", "<br>\n")

        message = Message(
            author = user,
            text = text,
            hike = hike,
        )

        message.save()

        return HttpResponseRedirect("/discussion/"+str(hike.id))




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
        context = base_context(request, title=hike.name)
        this_hike = {}

        # Сюда вставить все достопримечательности
        this_hike['landmarks'] = list(Landmark.objects.filter(is_public=True))
        if hike.image.name is not None and hike.image.name != "":
            this_hike['image'] = hike.image
        else:
            this_hike['image'] = ''
        days = []
        months = ['января', 'февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']
        
        
        for day in Day.objects.filter(hike=hike).order_by('date'):

            day_id = int(day.name.split()[1])

            if day_id == 1 or day.description !='' or day.caption != '':
                data = {}
                data['description'] = day.description
                data['header'] = day.caption
                data['date'] = str(day.date.day)+' '+months[day.date.month-1]
                data['name'] = day.name
                data['id'] = str(day_id)
                days.insert(0, data)
            else:

                if days[0]['date'].find(' - ')!=-1:
                    days[0]['date'] = days[0]['date'][:days[0]['date'].find(' - ')]

                if days[0]['name'].find(' - ')!=-1:
                    days[0]['name'] = days[0]['name'][:days[0]['name'].find(' - ')]

                # days[0]['name'].replace('День', 'Дни')

                days[0]['date']+=' - '+str(day.date.day)+' '+months[day.date.month-1]

                days[0]['name']+=' - '+str(day_id)


        days = sorted(days, key=lambda x: int(x['id']))

        for day in days:
            if day['date'].count(day['date'].split(' ')[-1])>1:
                date = day['date']
                month = day['date'].split(' ')[-1]
                day['date'] = date[:date.find(month)-1]+date[date.find(month)+len(month):]

        this_hike['days'] = days
        participants = []
        usernames = []


        for participant in hike.participants.all():
            usernames.append(participant.username)
            props = [full_name(participant), participant.username, '']
            if participant.profile.avatar.name != '':
                props[2] = participant.profile.avatar
            props.append("/account/" + participant.username)
            participants.append(props)

        this_hike['participants'] = participants
        this_hike['usernames'] = usernames

        if hike.limit_of_members - len(participants) > 0:
            this_hike['vacancies'] = hike.limit_of_members - len(participants)
            this_hike['free_plases'] = "Yup"
        else:
            this_hike['vacancies'] = 0
            this_hike['free_plases'] = "Nope"



        context['content'] = hike.__dict__
        context['content'].update(this_hike)
        context['content']['creator'] = hike.creator

        
        context['rus_date'] = beauty_date_interval(hike.start_date, hike.end_date, True, True)

        if 0<int(str(this_hike['vacancies'])[-1:])<5:
            context['number_of_free_places'] = str(this_hike['vacancies'])+' места'
        else:
            context['number_of_free_places'] = str(this_hike['vacancies'])+' мест'
        context['author_full_name'] = full_name(hike.creator)

        # Комментарии

        comments = []

        hike_comments_models = Message.objects.filter(hike=hike).order_by('creation_datetime')

        for ct_model in hike_comments_models:
            ct = {}
            ct['author'] = full_name(ct_model.author)
            ct['author_username'] = ct_model.author.username
            ct['comment'] = ct_model.text

            ct['avatar'] = ''
            if ct_model.author.profile.avatar.name != '':
                ct['avatar'] = ct_model.author.profile.avatar

            published_time = ct_model.creation_datetime.strftime('%H:%M, %d ')+months[ct_model.creation_datetime.month-1]
            ct['time_published'] = published_time
            comments.append(ct)
        context['comments'] = comments


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


class Account(View):

    def get(self, request, username):

        user = User.objects.get(username=username)

        cur_user = request.user

        # user = request.user
        months = ['января', 'февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']

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
        context['image'] = ''
        if user.profile.avatar.name != '':
            context['image'] = Profile.objects.get(user=user).avatar.url

        context['user'] = user
        context['cur_user'] = cur_user
        context['profile'] = profile
        context['full_name'] = full_name
        context['contacts'] = Contact.objects.filter(user=user)
        context['list_of_alowed_positions'] = ["phone", "telegram", "email"]
        # context['list_of_alowed_visible_conds'] = ["noone","friends","all"]

        posts = Post.objects.filter(post_author=user).order_by('creation_datetime')

        print(posts)

        users_posts = []

        for post in posts:
            ct = {}
            ct['content'] = post.content
            ct['author'] = post.post_author
            ct['author_fullname'] = full_name
            ct['author_username'] = post.post_author.username

            ct['avatar'] = ''
            if post.post_author.profile.avatar.name != '':
                ct['avatar'] = post.post_author.profile.avatar.url

            published_time = post.creation_datetime.strftime('%H:%M, %d ')+months[post.creation_datetime.month-1]
            ct['time_published'] = published_time
            users_posts.insert(0, ct)
        context['users_posts'] = users_posts

        return render(request, "account.html", context)

    def post(self, request, username):
        form = request.POST
        print(form)

        post = Post(
            post_author = request.user,
            content = form['post_content'],
            creation_datetime = datetime.now()
        )
        
        post.save()

        return HttpResponseRedirect("/account/" + username)



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


        context = base_context(request, title=full_name(user), header=username)
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
        return HttpResponseRedirect('/account/' + str(user.username))


class HikeFilter(View):
    def get(self, request):
        context = base_context(request, title='Поиск похода')
        
        return render(request, "hike_filter.html", context)