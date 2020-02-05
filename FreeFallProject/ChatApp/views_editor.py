from ChatApp.views import *


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
                if len(Profile.objects.filter(user=user)) and user.profile.avatar.name != '':
                    participants.append((user.username, user.profile.avatar))
                else:
                    participants.append((user.username, ''))

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

        hike_id = 1
        while 'day_'+str(hike_id)+'_name' in form.keys():
            name = 'day_'+str(hike_id)+'_name'
            if form[name] != '':
                new_day = Day(hike=hike, name=form[name], description=form)
                new_day.save()

            hike_id += 1

        # participants = participants_format(form['participants'])
        participants = participants_new_format(form['participants'])
        already_in_hike = hike.participants.all()
        for pt in participants:
            if pt not in already_in_hike:
                hike.participants.add(pt)
        hike.save()

        return HttpResponseRedirect("/hike/"+str(hike.id))