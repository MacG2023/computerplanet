from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import uuid

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    access_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    ticket_no = models.CharField(max_length=20, unique=True, blank=True , null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    subject = models.CharField(max_length=200)
    description = models.TextField()
    admin_notes = models.TextField(blank=True, null=True)   
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    reported_by = models.CharField(max_length=100, blank=True, null=True)
    attachment = models.FileField(upload_to='ticket_files/', blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} - {self.status}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Save first to get a primary key

        if is_new and not self.ticket_no:
            date_str = timezone.localtime(self.created_at).strftime('%y%m%d')
            self.ticket_no = f"CP{date_str}{self.id:04d}"
            # Save again to update ticket_no
            super().save(update_fields=['ticket_no'])

        else:
            old_ticket = Ticket.objects.get(pk=self.pk)
            if old_ticket.status != self.status:
                send_mail(
                    subject="Ticket Update - Computer Planet",
                    message=f"Hi {self.customer.username},\n\nYour ticket '{self.subject}' status has been updated to '{self.status}'.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[self.customer.email],
                    fail_silently=True,
                )
