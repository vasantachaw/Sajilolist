from django.contrib import admin
from ContactUs.models import ContactUs,Company
from ContactUs.models import JobVacancy



@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'district', 'is_verified', 'created_at')
    search_fields = ('name', 'city', 'district', 'phone', 'email')
    list_filter = ('is_verified', 'city', 'district', 'created_at')


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_at',)



@admin.register(JobVacancy)
class JobVacancyAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "application_deadline")

