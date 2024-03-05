from django.db import models
from django.contrib.auth.models import User
from student.models import StudentProfile
from django.core.validators import MinValueValidator, MaxValueValidator

class PropertyReview(models.Model):
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property.name} - {self.reviewer.user.username}"

class RoommateReview(models.Model):
    roommate = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='reviews_given')
    reviewer = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='reviews_received')
    text = models.TextField()
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.roommate.user.username} - {self.reviewer.user.username}"

class StudentReview(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey('property.Property', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.reviewer.name}"