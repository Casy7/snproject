from django.contrib import admin
from .models import *

# Для регистрации модели добавить её в models
models = [

]

for model in models:
    admin.site.register(model)