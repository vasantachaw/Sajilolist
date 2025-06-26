from django.shortcuts import render, redirect
from authentication.models import Profile
from django.contrib.auth.models import User
from authentication.mixsins import MessageHandler
import random
from django.contrib.auth import login,authenticate
from django.contrib import messages
import re

import logging
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
# Create your views here.
import logging
logger = logging.getLogger(__name__)




# def login_view(request):
#     if request.method == "POST":
#         phone = request.POST.get("phone", "").strip()

#         if not phone:
#             messages.error(request, "Please enter your phone number.")
#             return redirect("login")

#         try:
#             profile = Profile.objects.get(phone_number=phone)
#         except Profile.DoesNotExist:
#             messages.error(request, "Phone number not registered.")
#             return redirect("login")

#         full_phone = profile.country + phone
#         print(f"Full phone number for OTP: {full_phone}")
#         logger.info(f"Full phone number for OTP: {full_phone}")

#         # Generate and save OTP
#         otp = str(random.randint(1000, 9999))
#         profile.otp = otp
#         profile.save()

#         # Send OTP via Vonage SMS
#         sid = MessageHandler(full_phone, otp).send_otp_on_phone()
#         if sid:
#             logger.info(f"OTP sent successfully to {full_phone} with SID: {sid}")
#             messages.success(request, "OTP sent to your phone.")
#             return redirect("otp-verify", uid=profile.uid)
#         else:
#             logger.error(f"Failed to send OTP to {full_phone}")
#             messages.error(request, "Failed to send OTP. Please try again.")
#             return redirect("login")

#     return render(request, "auth/index.html")






def login_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if not phone or not password:
            messages.error(request, "Phone and password are required.")
            return redirect("login")

        try:
            profile = Profile.objects.get(phone_number=phone)
            user = profile.user
        except Profile.DoesNotExist:
            messages.error(request, "Phone number not registered.")
            return redirect("login")

        if check_password(password, user.password):
            if not user.is_active:
                messages.error(request, "Your account is inactive. Please activate your account.")
                return redirect("login")

            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        else:
            messages.error(request, "Incorrect password.")
            return redirect("login")

    return render(request, "auth/index.html")



def is_valid_phone(phone, country):
    if country == "+977":
        # Nepal (NTC/Ncell): includes 97, 98[04568], 981, 982
        return re.fullmatch(r"(97\d|98[04568]|981|982)\d{7}", phone) is not None
    elif country == "+1":
        # USA: 10 digits, starts with 2–9
        return re.fullmatch(r"[2-9]\d{9}", phone) is not None
    return False  # Default reject unknown codes

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "").strip()
        country = request.POST.get("country_code", "").strip()
        print(f"Username: {username}")
        print(f"Phone: {phone}")
        print(f"Country Code: {country}")
        print(f"Password: {password}") 

        if not username or not phone or not country or not password:
            messages.warning(request, "All fields are required.")
            return redirect("register")

        if not is_valid_phone(phone, country):
            messages.warning(request, "Invalid phone number format for selected country.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already taken. Please choose another.")
            return redirect("register")

        if Profile.objects.filter(phone_number=phone).exists():
            messages.warning(request, "Phone number already used.")
            return redirect("register")

        try:
            user = User.objects.create_user(username=username, password=password)
            Profile.objects.create(
                user=user, phone_number=phone, country=country
            )
            #user.is_active = False  # Set inactive until OTP verification, if applicable
            user.save()
            messages.success(request, "Registration successful.")
            return redirect("login")
        except Exception as e:
            logger.warning(f"Registration failed: {e}")
            messages.warning(request, "Registration failed. Please try again.")
            return redirect("register")

    return render(request, "auth/index.html")


def logout_view(request):
    logout(request)
    # Redirect to home page or any other page after logout
    return redirect("home")


def otp_view(request, uid):
    try:
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        messages.error(request, "Invalid request.")
        return redirect("login")

    if request.method == "POST":
        # Combine all digits
        otp = "".join(
            [request.POST.get(f"otp_digit_{i}", "").strip() for i in range(1, 5)]
        )

        if not otp.isdigit() or len(otp) != 4:
            messages.error(request, "OTP must be a 6-digit number.")
            return redirect("otp-verify", uid=uid)

        if otp == profile.otp:
            login(request, profile.user)
            profile.otp = ""  # Invalidate OTP after use
            profile.save()
            messages.success(request, "Login successful.")
            return redirect("home")
        else:
            messages.error(request, "Invalid OTP.")
            return redirect("otp-verify", uid=uid)

    return render(request, "auth/otp_verify.html", {"uid": uid})

def otp(request):
    return render(request, "auth/otp_verify.html")

def profile_view(request):
    return render(request, "auth/profile.html")


def forget_password_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone", "").strip()

        if not phone:
            messages.error(request, "Please enter your phone number.")
            return redirect("forgot-password")

        try:
            profile = Profile.objects.get(phone_number=phone)
        except Profile.DoesNotExist:
            messages.error(request, "Phone number not registered.")
            return redirect("forgot-password")

        # Construct full phone number (e.g., with country code)
        full_phone = profile.country + phone
        logger.info(f"Full phone number for OTP: {full_phone}")

        # Generate 4-digit OTP
        otp = str(random.randint(1000, 9999))
        profile.otp = otp
        profile.save()

        # Send OTP via Vonage SMS
        sid = MessageHandler(full_phone, otp).send_otp_on_phone()
        if sid:
            logger.info(f"OTP sent successfully to {full_phone} with SID: {sid}")
            messages.success(request, "OTP sent to your phone.")
            return redirect("otp-verify", uid=profile.uid)
        else:
            logger.error(f"Failed to send OTP to {full_phone}")
            messages.error(request, "Failed to send OTP. Please try again.")
            return redirect("forgot-password")

    # GET request: render forgot password form
    return render(request, "auth/forgot_password.html")