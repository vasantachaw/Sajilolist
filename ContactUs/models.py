from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

class Company(models.Model):
    name = models.CharField(max_length=200)
    description = CKEditor5Field(config_name='extends')
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    # Social media
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name



class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_us')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.name} ({self.email})"




class JobVacancy(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = CKEditor5Field(config_name='extends')
    qualifications = CKEditor5Field(config_name='extends')
    experience_required = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    application_deadline = models.DateField()
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    listed_date = models.DateField(auto_now_add=True)
    
    image1 = models.ImageField(upload_to='jobvacancy_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='jobvacancy_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='jobvacancy_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='jobvacancy_images/', blank=True, null=True)
    image5 = models.ImageField(upload_to='jobvacancy_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"
