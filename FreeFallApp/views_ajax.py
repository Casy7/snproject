from .models import *
from .forms import *
from FreeFallApp.views import *
import base64
from FreeFallProject.settings import MEDIA_ROOT, MEDIA_URL


class NotificationResult(View):
    def post(self, request):
        req = request
        form = request.POST
        code = form['code']
        decode_code = code.split('-')
        user = request.user
        hike = Hike.objects.get(id=decode_code[1])

        result = {}
        # for notification in nt:
        if decode_code[2] == 'invite_to_hike':
            if form['result'] == 'agree':
                notification = Notification.objects.filter(user=user).filter(
                    from_user__id=decode_code[0]).filter(hike__id=decode_code[1])[0]
                hike.participants.add(user)
                notification.delete()
                result['result'] = 'success'
            elif form['result'] == 'disagree':
                notification = Notification.objects.filter(user=user).filter(
                    from_user__id=decode_code[0]).filter(hike__id=decode_code[1])[0]
                notification.delete()
                result['result'] = 'success'
            elif form['result'] == 'delete':
                if User.objects.get(id = decode_code[0]) in hike.participants.all():
                    hike.participants.remove(User.objects.get(id = decode_code[0]))
                else:
                    while len(Notification.objects.filter(from_user=user).filter(user__id=decode_code[0]).filter(hike__id=decode_code[1])):
                        notification = Notification.objects.filter(from_user=user).filter(
                            user__id=int(decode_code[0])).filter(hike__id=decode_code[1])[0]
                        notification.delete()
                result['result'] = 'success'
        if decode_code[2] == 'request_for_ptc':
            if form['result'] == 'create' and len(Notification.objects.filter(user=user).filter(from_user__id=decode_code[0]).filter(hike__id=decode_code[1])) == 0:
                if hike.join_to_group == 'open':
                    hike.participants.add(user)
                    hike.save()
                    result['result'] = 'success'
                    ptc_list = []
                    for user in hike.participants.all():
                        ptc_list.append(full_name(user))
                    result['users'] = ptc_list

                elif hike.join_to_group == 'request':
                    nt = Notification(
                        user=hike.creator, type_of_notification='request_for_ptc', from_user=user, hike=hike)
                    nt.save()
                    result['result'] = 'success'
                    ptc_list = []
                    for user in hike.participants.all():
                        ptc_list.append(full_name(user))
                    result['users'] = ptc_list
                elif hike.join_to_group == 'close':
                    result['result'] = 'error'
            elif form['result'] == 'agree':
                from_user = decode_code[0]
                hike.participants.add(from_user)
                nt = Notification.objects.filter(user=user).filter(
                    from_user__id=decode_code[0]).filter(hike__id=decode_code[1])
                for notification in nt:
                    nt.delete()

        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )


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
                with open(os.path.join(MEDIA_ROOT,image.name), "rb") as img_file:
                    my_string = base64.b64encode(
                        img_file.read()).decode("ASCII")
                    result['image'] = my_string


            result['full_name'] = full_name(user)
            result['id'] = user.id
            if 'add_to_hike' in form.keys() and form['add_to_hike'] == 'true':
                hike_id = form['hike_id']
                if len(Notification.objects.filter(hike=Hike.objects.get(id=hike_id)).filter(user=user).filter(type_of_notification='invite_to_hike')) == 0:
                    nt=Notification(user=user,
                                    hike=Hike.objects.get(id=hike_id),
                                    type_of_notification='invite_to_hike',
                                    from_user=request.user)
                    nt.save()
        else:
            result['exist']='False'
        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )


class IsNewHikeValid(View):
    def post(self, request):
        req=request
        form=HikeForm(request.POST)
        if form.is_valid():
            pass
        result={}
        if len(User.objects.filter(username=form['username'])) > 0:
            result['exist']='True'
        else:
            result['exist']='False'
        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )


class SendNotifications(View):
    def post(self, request):
        form=request.POST
        user=request.user
        result={}
        if user.is_anonymous == False:

            result['result'] = 'success'
            result['notifications']=notifications_to_js_format(
                check_notifications(user))

        else:
            result['result'] = 'fail'
            result['notifications']=[]
        return HttpResponse(json.dumps(result), content_type="application/json")

    
class ChangeMap(View):
    def post(self, request):
        form=request.POST
        user=request.user
        result={}
        if user.is_anonymous == False:
            if form['operation'] == 'delete_landmark':
                lmk_id = int(form['lmk_id'])
                Landmark.objects.get(id = lmk_id).delete()
                result['result'] = 'success'
            elif form['operation'] == 'add_landmark':
                lmk = Landmark(
                    name = form['lmk_name'],
                    description = form['lmk_desc'],
                    longitude = form['lat'],
                    latitude= form['lon']
                )
                lmk.save()
                result['result'] = 'success'
        else:
            result['result'] = 'fail'
        return HttpResponse(json.dumps(result), content_type="application/json")


class FilterHikes(View):
    def post(self, request):
        result = {}
        filter_dict = request.POST
        # Временной фильтр
        hikes = Hike.objects.filter(end_date__lte=filter_dict['end_day']).filter(start_date__gte=filter_dict['start_day'])
        # print(len(hikes))
        # Этот фрагмент отвечает за фильтр категории сложности похода
        all_categories = ['none','I','II','III','IV','V','VI']
        selected_categories = all_categories[all_categories.index(filter_dict['min_category']):all_categories.index(filter_dict['max_category'])+1]
        filter_cat = 'Q(difficulty=\''+selected_categories[0]+'\')'
        if len(selected_categories)>1:
            for cat in selected_categories[1:]:
                filter_cat+='|Q(difficulty=\''+cat+'\')'

        hikes = hikes.filter(eval(filter_cat))
        # print(len(hikes))
        # Фильтр типа похода (пеший/горный/водный т.п.)
        
        types = filter_dict['types'].split(',')
        filter_type = 'Q(type_of_hike=\''+types[0]+'\')'
        if len(types)>1:
            for hike_type in types[1:]:
                filter_type+='|Q(type_of_hike=\''+hike_type+'\')'
        
        hikes = hikes.filter(eval(filter_type))
        # print(len(hikes))

        # Фильтры свободы добавления
        if filter_dict['show_hikes_with_close_members_entry'] == 'false':
            hikes = hikes.filter(Q(join_to_group='open')|Q(join_to_group='request'))
        if filter_dict['show_hikes_with_entry_by_request'] == 'false':
            hikes = hikes.filter(Q(join_to_group='open')|Q(join_to_group='close'))

        # Фильтр, удаляющий из списка походы со сформированными группами
        if filter_dict['show_hikes_with_completed_groups'] == 'false':
            for hike in hikes:
                if hike.limit_of_members == len(hike.participants.all())+len(Notification.objects.filter(hike=hike)):
                    hikes.remove(hike)

        # Фильтр поиска по ключевым словам

        if filter_dict['name'] != '':
            names = []
            descs = []
            for hike in hikes:
                names.append(hike.name)
                descs.append(hike.description)
            
            keywords = filter_dict['name'].lower().split(' ')
            # Основная часть фильтра
            valid_hikes = []

            for index in range(len(names)):

                name = names[index].lower()
                overlap = 0
                hike_header = names[index].lower()
                
                if name.split(' ') == keywords:
                    valid_hikes.append(hikes[index])
                    continue

                for keyword in keywords:
                    keyword = cut_keyword(keyword)      # TODO написать сию чудесатую функцию
                    if keyword in hike_header:
                        if len(keyword)<=3:
                            overlap+=1
                        else:
                            overlap+=2
                if overlap/len(keywords)>1:
                    valid_hikes.append(hikes[index])
            hikes = valid_hikes
                
        # print(hikes)
        result['result']= 'success'
        json_format_hikes = []
        for hike in hikes:
            json_format_hikes.append(hike_to_json(hike))
        result['hikes'] = json_format_hikes
        # print(result)
        return HttpResponse(json.dumps(result), content_type="application/json")



class AddComment(View, LoginRequiredMixin):
    def post(self, request):
        result = {}
        
        comment_props = request.POST

        if comment_props['comment'] != '':
            model = Message(text=comment_props['comment'], author=request.user, hike=Hike.objects.get(id=int(comment_props['hike'])))
            model.save()
            result['result'] = 'success'
            result['author'] = full_name(request.user)
            months = ['января', 'февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']
            result['time_published'] = model.creation_datetime.strftime('%H:%M, %d ')+months[model.creation_datetime.month-1]



        return HttpResponse(json.dumps(result), content_type="application/json")
