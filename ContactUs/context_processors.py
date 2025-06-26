from ContactUs import models
def contact_us_context(request):
    """
    Context processor to add contact us information to the context.
    """
    contact_info = models.ContactUs.objects.first()
    company_info = models.Company.objects.first()
    return {
        'contact_info': contact_info,
        'companyinfo': company_info,
    }