from .models import *
from .forms import *
import base64
import os
from FreeFallProject.settings import MEDIA_ROOT, MEDIA_URL, BASE_DIR

# def set_notification(user, type_of_notification, from_user = None , hike = None, *args):
#     new_notification = Notification(user, type_of_notification,)
#     return 0

def check_notifications(user):
    return list(Notification.objects.filter(user = user))


def notifications_to_js_format(nt_list):
    result_list = []
    for notification in nt_list:
        new_format_nt = []
        new_format_nt.append(notification.type_of_notification)
        if notification.type_of_notification in ["invite_to_hike","request_for_ptc","user_added_to_hike"]:
                        
            user=notification.from_user
            new_format_nt.append(full_name(user))
            new_format_nt.append(user.id)
            new_format_nt.append(notification.hike.name)
            new_format_nt.append(notification.hike.id)
            if len(Profile.objects.filter(user = user))>0 and user.profile.avatar.name!='':
                image = user.profile.avatar
                with open(os.path.join(BASE_DIR, 'FreeFallApp\\user_files\\')+image.name.replace('/','\\'), "rb") as img_file:
                    my_string = base64.b64encode(img_file.read()).decode("ASCII")
                new_format_nt.append(my_string)
                # str(new_format_nt.append(user.profile.avatar))
            else:
                new_format_nt.append('')
            new_format_nt.append(str(notification.datetime))
            result_list.append(new_format_nt)
        elif notification.type_of_notification == "simple_text":

            result_list.append(new_format_nt)
                   

    return result_list




            
def full_name(user):
    if user.last_name != '' and user.first_name != '':
        return user.first_name+' '+user.last_name
    elif user.first_name != '':
        return user.first_name
    elif user.last_name != '':
        return user.last_name
    else:
        return user.username


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
        context['notifications'] = notifications_to_js_format(check_notifications(user))
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


def hike_to_json(hike):
    result = {}
    # hike = Hike.object.get(id=1)
    result['id'] = hike.id
    result['name'] = hike.name
    result['description'] = hike.description
    result['creator'] = full_name(hike.creator)
    result['start_date'] = hike.start_date.strftime("%d of %B, %Y")
    result['end_date'] = hike.end_date.strftime("%d of %B, %Y")

    if hike.image.name!='':
        try:
            result['image'] = base64.b64encode(hike.image.read()).decode("ASCII")
        except FileNotFoundError:
            result['image'] = ''
    else:
        result['image'] = ''

    return result


def cut_keyword(word):
    if len(word)<=3:
        return word
    elif len(word)<=5:
        return word[:-1]
    elif len(word)<=7:
        return word[:-2]
    else:
        return word[:-3]

