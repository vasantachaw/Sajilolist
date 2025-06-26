from django.db import models
from django.contrib.auth.models import User
import uuid
from django.templatetags.static import static

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    country = models.CharField(max_length=5)
    otp = models.CharField(max_length=6, blank=True, null=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    profile_picture = models.ImageField(upload_to='agents/', blank=True, null=True)
    website = models.URLField(max_length=200, blank=True)
    social_media = models.JSONField(blank=True, null=True)

    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    # New fields
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.country} {self.phone_number}"

    def full_contact_info(self):
        return f"Phone: {self.phone_number}, Email: {self.email}, Website: {self.website}"

    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        return static('images/default_profile_picture.jpg')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
