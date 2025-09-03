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



from .forms import UserRegisterForm, ProfileForm, CustomPasswordResetForm

from .tokens import account_activation_token


from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email").lower()

            # ✅ Check if email already exists
            if User.objects.filter(username=email).exists():
                messages.error(
                    request,
                    "This email is already registered. Please log in or reset your password if you've forgotten it."
                )
                return render(request, 'accounts/registration/register.html', {'form': form})

            # ✅ Create user with email as username
            user = form.save(commit=False)
            user.username = email
            user.email = email
            user.is_active = False  # wait until email activation
            user.save()

            # ✅ Build activation link
            current_site = get_current_site(request)
            subject = "Activate your Computer Planet account"

            html_message = render_to_string('accounts/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            plain_message = strip_tags(html_message)

            # ✅ Send email with HTML + plain-text fallback
            email_message = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email_message.attach_alternative(html_message, "text/html")
            email_message.send()

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

        return render(request, 'accounts/registration/account_activation_invalid.html')



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

