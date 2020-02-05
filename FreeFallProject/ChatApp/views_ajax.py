from .models import *
from .forms import *
from ChatApp.views import *

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
                    my_string = base64.b64encode(
                        img_file.read()).decode("ASCII")
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


