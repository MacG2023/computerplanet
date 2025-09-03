from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import PasswordResetForm

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Profile
from django.core.mail import EmailMultiAlternatives



class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):

        subject = render_to_string(subject_template_name, context).strip()
        html_message = render_to_string(email_template_name, context)
        plain_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject, plain_message, from_email, [to_email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()



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







class ProfileForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = ["name", "phone", "company", "address"]

        widgets = {

            "name": forms.TextInput(attrs={"class": "form-control"}),

            "address": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),

            "phone": forms.TextInput(attrs={"class": "form-control"}),

            "company": forms.TextInput(attrs={"class": "form-control"}),

        }

