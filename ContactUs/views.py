# views.py
from django.shortcuts import render,HttpResponse
from ContactUs.forms import ContactUsForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def contact_us_view(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            home_url = reverse('home')  # resolve URL name 'home' to path, e.g. '/'
            return HttpResponse(f"""
                <script>
                    alert('Successful leave your message!');
                    window.location.href = '{home_url}';
                </script>
            """)
    else:
        form = ContactUsForm()
    return render(request, "contactus/contact.html", {"form": form})
