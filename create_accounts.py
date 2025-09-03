import os

BASE_DIR = os.path.join(os.getcwd(), "accounts")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates", "registration")

# Directory structure
dirs = [
    BASE_DIR,
    os.path.join(BASE_DIR, "migrations"),
    os.path.join(BASE_DIR, "templatetags"),
    TEMPLATES_DIR,
]

# Files with boilerplate content
files_content = {
    os.path.join(BASE_DIR, "__init__.py"): "",
    os.path.join(BASE_DIR, "forms.py"): """from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # username = email
        user.email = self.cleaned_data['email']
        user.is_active = False  # require email confirmation
        if commit:
            user.save()
        return user
""",
    os.path.join(BASE_DIR, "views.py"): """from django.contrib.auth import login
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

from .forms import UserRegisterForm
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
    return render(request, 'registration/register.html', {'form': form})

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
""",
    os.path.join(BASE_DIR, "urls.py"): """from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
""",
    os.path.join(BASE_DIR, "tokens.py"): """from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)

account_activation_token = AccountActivationTokenGenerator()
""",
    # Templates
    os.path.join(TEMPLATES_DIR, "login.html"): "<h2>Login Page</h2>{% block content %}{% endblock %}",
    os.path.join(TEMPLATES_DIR, "register.html"): "<h2>Register Page</h2>{% block content %}{% endblock %}",
    os.path.join(TEMPLATES_DIR, "account_activation_email.html"): "Hi {{ user.username }}, click here to activate: http://{{ domain }}{% url 'activate' uidb64=uid token=token %}",
    os.path.join(TEMPLATES_DIR, "account_activation_invalid.html"): "<h2>Activation link is invalid!</h2>",
    os.path.join(TEMPLATES_DIR, "password_reset_form.html"): "<h2>Password Reset Form</h2>",
    os.path.join(TEMPLATES_DIR, "password_reset_done.html"): "<h2>Password Reset Email Sent</h2>",
    os.path.join(TEMPLATES_DIR, "password_reset_confirm.html"): "<h2>Password Reset Confirm</h2>",
    os.path.join(TEMPLATES_DIR, "password_reset_complete.html"): "<h2>Password Reset Complete</h2>",
}

# Create dirs
for d in dirs:
    os.makedirs(d, exist_ok=True)

# Write files
for path, content in files_content.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Accounts app structure generated successfully!")
