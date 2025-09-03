from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    # Add a file upload field
    attachment = forms.FileField(
        required=False,  # optional
        label="Attach a file (optional)"
    )

    class Meta:
        model = Ticket
        fields = ["status", "subject", "description",  "reported_by", "attachment"]  # include attachment




class TicketFormUpdate(forms.ModelForm):
    # Add a file upload field
    attachment = forms.FileField(
        required=False,  # optional
        label="Attach a file (optional)"
    )

    class Meta:
        model = Ticket
        fields = ["status", "subject", "description", "admin_notes", "reported_by", "attachment"] 

class AdminTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["status", "admin_notes"]
