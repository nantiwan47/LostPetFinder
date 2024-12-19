from django.contrib import admin

from petfinder.models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(PetAnnouncement)
admin.site.register(Notification)