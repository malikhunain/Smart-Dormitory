from django.contrib import admin

# Register your models here.

from .models import Property, Room, Media, Amenities, PropertyOwnerProfile, RoomType

admin.site.register(Property)
admin.site.register(Room)
admin.site.register(Media)
admin.site.register(Amenities)
admin.site.register(PropertyOwnerProfile)
admin.site.register(RoomType)

