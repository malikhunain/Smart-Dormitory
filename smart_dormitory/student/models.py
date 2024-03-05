from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    email = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    religion = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='static/profile_pictures/', null=True, blank=True)
    age = models.IntegerField(blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)
    academic_level = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Freshman, Sophomore, Graduate Student")
    major = models.CharField(max_length=100, blank=True, null=True, help_text="Your academic major or field of study")
    interests = models.TextField(blank=True, null=True, help_text="List your hobbies and interests")
    preferred_roommate = models.TextField(blank=True, null=True, help_text="List your preferred roommate's interests, hobbies, and other characteristics")
    cleanliness_level = models.IntegerField(blank=True, null=True, help_text="Rate your cleanliness on a scale of 1 to 5")
    smoking_preference = models.BooleanField(default=False, help_text="Do you prefer a non-smoking environment?")
    reviews_by_roommates = models.ManyToManyField('review.RoommateReview', related_name='student_reviews', blank=True)
    reviews_by_property_owners = models.ManyToManyField('review.StudentReview', related_name='student_reviews', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
