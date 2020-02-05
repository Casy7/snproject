from .models import *
from .forms import *


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
                new_format_nt.append(notification.hike.id)
            else:
                new_format_nt.append('')
            new_format_nt.append(notification.datetime)
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


