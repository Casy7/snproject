from FreeFallApp.views import *


class HikeEditor(View, LoginRequiredMixin):
    def get(self, request, id):

        hike = Hike.objects.get(id=id)

        context = base_context(
            request, title='Track')
        context['id'] = hike.id
        if hike.image.name is not None:
            context['image'] = hike.image
        else:
            context['image'] = ''

        if context['username'] != '' and request.user == hike.creator:
            participants = []
            for user in hike.participants.all():
                if len(Profile.objects.filter(user=user)) and user.profile.avatar.name != '' and  os.path.isfile(user.profile.avatar.path):
                    participants.append(
                        (full_name(user), user.profile.avatar, user.username, user.id))
                else:
                    participants.append(
                        (full_name(user), '', user.username, user.id))

            user_list = []

            ptcs = result = map(lambda x: x[2], hike.participants.all())
            for user in User.objects.all().exclude(notification__hike=hike).exclude(hike=hike):
                user_details = [user.username, full_name(user)]
                if len(Profile.objects.filter(user=user)) and  user.profile.avatar.name != '' and  os.path.isfile(user.profile.avatar.path):
                    
                    user_details.append(user.profile.avatar)
                else:
                    user_details.append('')
                user_list.append(user_details)

            context['user_list'] = user_list

            pot_ptc_list = Notification.objects.filter(
                hike=hike).filter(type_of_notification='invite_to_hike')
            pot_users = []
            for nt in pot_ptc_list:
                if len(Profile.objects.filter(user=nt.user)) and nt.user.profile.avatar.name != '':
                    pot_users.append(
                        (full_name(nt.user), nt.user.profile.avatar, nt.user.username, nt.user.id))
                else:
                    pot_users.append(
                        (full_name(nt.user), '', nt.user.username, nt.user.id))

            context['potential_ptc'] = pot_users
            days = []

            for day in Day.objects.filter(hike=hike):

                ide = int(day.name.split()[1])

                data = {}
                if day.image.name is not None and day.image.name != "":
                    data['image'] = day.image
                else:
                    data['image'] = ''
                data['description'] = day.description
                data['caption'] = day.caption
                #data['date'] = day.date
                data['coordinates'] = day.coordinates
                data['fake_name'] = str('Day' + day.name.split()[1])
                data['name'] = day.name
                data['id'] = str(ide)
                data['idn'] = int(ide)
                data['label'] = 'day' + str(ide)
                ide += 1
                days.insert(0, data)

            days = sorted(days, key=lambda x: x['idn'])

            context.update({
                'name': hike.name,
                'hike_id': hike.id,
                'short_description': hike.short_description,
                'start_date': str(hike.start_date),
                'end_date': str(hike.end_date),
                'difficulty': hike.difficulty,
                'type_of_hike': hike.type_of_hike,
                'limit_of_members': int(hike.limit_of_members),
                'participants': participants,
                'landmarks': list(Landmark.objects.filter(is_public=True)),
                'description': hike.description,
                'days': days,
                'coordinates': hike.coordinates,
                'join_to_group': hike.join_to_group
            })

            return render(request, "editor.html", context)

        else:
            return HttpResponseRedirect("/login/")

    def post(self, request, id):

        form = request.POST

        print(form)
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
        hike.limit_of_members = form['limit_of_members']
        hike.description = form['description']
        hike.start_date = form['start']
        hike.end_date = form['end']
        hike.difficulty = form['difficulty']
        hike.type_of_hike = form['type']
        hike.join_to_group = form['can_users_join']
        coordinates = str(form['coordinates'])
        data = coordinates.split(',')
        coordinates = []
        for i in range(len(data)//4):
            coordinates.append(
                [str(data[i*4]), int(data[i*4+1]), [float(data[i*4+2]), float(data[i*4+3])]])

        delete = str(form['cord_del'])
        # print(delete)
        data = delete.split(',')
        # print(data)
        delete = []

        end_coordinates = []

        for el in data:
            for marker in coordinates:
                if marker[0] == el:
                    coordinates.remove(marker)
                    break

        for el in coordinates:
            end_coordinates.append([el[1], el[2]])

        hike.coordinates = end_coordinates
        hike.save()

        for day in Day.objects.filter(hike=hike):
            ide = int(day.name.split()[1])
            day.caption = form['day' + str(ide) + '_caption']
            day.description = form['day' + str(ide) + '_description']
            day.save()
            ide += 1
        hike.save()

        return HttpResponseRedirect("/hike/"+str(hike.id))
