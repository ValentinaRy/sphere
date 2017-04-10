from django.contrib import admin
from shelters.models import Shelter, Pet, Volunteer_work, Rating

admin.site.register(Shelter)
admin.site.register(Volunteer_work)
admin.site.register(Pet)
admin.site.register(Rating)


