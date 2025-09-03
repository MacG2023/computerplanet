from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from .models import Profile

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
