from django.contrib import admin
from .models import *

# Для регистрации модели добавить её в models
models = [Hike, Landmark, Profile,Contact, Day, Notification, Message, Post
]

for model in models:
    admin.site.register(model)