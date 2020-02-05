from .models import *
from .forms import *




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