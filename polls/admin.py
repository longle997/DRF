from django.contrib import admin
from .models import Poll, Choise

# Register your models here. register mean that you can interact with those models in admin page
admin.site.register(Poll)
admin.site.register(Choise)