from django.db import models
from django.contrib.auth.models import User
from review.models import RoommateReview
from student.models import StudentProfile

class PropertyOwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reviews = models.ManyToManyField(RoommateReview, related_name='property_owner_reviews', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Amenities(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='static/amenities_icons/', null=True, blank=True)

    def __str__(self):
        return self.name

class Property(models.Model):
    owner = models.ForeignKey(PropertyOwnerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    images_or_videos = models.ManyToManyField('Media', related_name='property_media', blank=True)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    description = models.TextField()
    gender = models.CharField(max_length=255, default='mixed')
    amenities = models.ManyToManyField(Amenities)
    room = models.ManyToManyField('Room', related_name='property_rooms', blank=True)
    review = models.ManyToManyField('review.PropertyReview', related_name='property_reviews', blank=True)
    
    def __str__(self):
        return self.name
    
class RoomType(models.Model):
    name = models.CharField(max_length=255)
    count = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=255)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms', default=1)
    images_or_videos = models.ManyToManyField('Media', related_name='room_media', blank=True)
    description = models.TextField()
    amenities = models.ManyToManyField(Amenities)
    room_dimensions = models.CharField(max_length=255)
    occupancy = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    roommates = models.ManyToManyField(StudentProfile, related_name='rooms', blank=True)

    def __str__(self):
        return self.name

class Media(models.Model):
    file = models.FileField(upload_to='static/media_files/')

    def __str__(self):
        return self.file.name