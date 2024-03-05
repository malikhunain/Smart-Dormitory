from django.contrib import admin

# Register your models here.

from .models import PropertyReview, RoommateReview, StudentReview

admin.site.register(PropertyReview)
admin.site.register(RoommateReview)
admin.site.register(StudentReview)