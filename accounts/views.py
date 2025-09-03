from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile

from .forms import UserRegisterForm, ProfileForm
from .tokens import account_activation_token

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            subject = 'Activate your Computer Planet account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            messages.info(request, 'Please confirm your email address to complete registration.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/registration/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated!')
        return redirect('home')
    else:
        return render(request, 'registration/account_activation_invalid.html')





def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "accounts/profile.html", {"profile": profile})

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Named URL for profile page
    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/profile.html", {"form": form})



@login_required
def profile_update(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/profile_update.html", {"form": form})
