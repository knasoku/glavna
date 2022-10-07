from django.contrib import admin

# Register your models here.
from .models import *
from upravitel.models import *

admin.site.register(Poll)
admin.site.register(Zgrada)
admin.site.register(Stanar)
admin.site.register(Upravitel)
admin.site.register(Announcement)