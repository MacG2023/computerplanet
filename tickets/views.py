from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Ticket
from .forms import TicketForm, AdminTicketForm, TicketFormUpdate
from django.contrib.admin.views.decorators import staff_member_required
import csv
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
import uuid

from django.urls import reverse

@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.customer = request.user
            ticket.save()

            messages.success(request, "Your ticket has been submitted!")

            # Build ticket URL with uuid
            ticket_url = request.build_absolute_uri(
                reverse("tickets:details_with_key", args=[ticket.pk, ticket.access_key])
            )

            # -----------------------
            # Email to Customer
            # -----------------------
            subject_customer = f"Your Support Ticket #{ticket.ticket_no} Has Been Created"

            text_body_customer = (
                f"Hi {ticket.reported_by or request.user.username},\n\n"
                f"Your ticket '{ticket.subject}' has been logged successfully.\n"
                f"Status: {ticket.get_status_display()}\n\n"
                f"You can view your ticket here: {ticket_url}\n\n"
                f"We will get back to you soon.\n\n"
                f"- Computer Planet"
            )

            html_body_customer = f"""
                <div style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                    <h2 style="color: #0d6efd;">Computer Planet Support</h2>
                    <p>Hi <strong>{ticket.reported_by or request.user.username}</strong>,</p>
                    <p>Thank you for reaching out. Your support ticket has been created successfully.</p>
                    
                    <table style="border-collapse: collapse; width: 100%; margin: 15px 0;">
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Ticket No</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;"><a href="{ticket_url}">#{ticket.ticket_no}</a></td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Subject</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{ticket.subject}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Status</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{ticket.get_status_display()}</td>
                        </tr>
                    </table>

                    <p>You can view your ticket here:</p>
                    <p>
                        <a href="{ticket_url}" >
                            View Ticket
                        </a>
                    </p>

                    <p style="margin-top:20px;">We’ll get back to you soon.<br>- <em>Computer Planet Team</em></p>
                </div>
            """

            email = EmailMultiAlternatives(
                subject=subject_customer,
                body=text_body_customer,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[request.user.email],
            )
            email.attach_alternative(html_body_customer, "text/html")
            email.send()

            # -----------------------
            # Email to Admin
            # -----------------------
            subject_admin = f"New Support Ticket #{ticket.ticket_no} Logged"
            text_body_admin = (
                f"A new ticket has been created by {request.user.email}.\n\n"
                f"Subject: {ticket.subject}\n"
                f"Description: {ticket.description}\n"
                f"Link: {ticket_url}"
            )

            html_body_admin = f"""
                <div style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                    <h2 style="color: #dc3545;">New Support Ticket Logged</h2>
                    <p>A new support ticket has been submitted.</p>
                    
                    <table style="border-collapse: collapse; width: 100%; margin: 15px 0;">
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Customer</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{request.user.email}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Ticket No</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">#{ticket.ticket_no}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Subject</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{ticket.subject}</td>
                        </tr>
                    </table>

                    <p>
                        <a href="{ticket_url}" style="display:inline-block; padding:10px 15px; background:#dc3545; color:#fff; text-decoration:none; border-radius:5px;">
                            View Ticket
                        </a>
                    </p>
                </div>
            """

            email_admin = EmailMultiAlternatives(
                subject=subject_admin,
                body=text_body_admin,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL],
            )
            email_admin.attach_alternative(html_body_admin, "text/html")
            email_admin.send()

            return redirect("tickets:my_tickets")
    else:
        form = TicketForm()

    return render(request, "tickets/create_ticket.html", {"form": form})

@login_required
def my_tickets(request):
    if request.user.is_staff:
        tickets = Ticket.objects.all().order_by("-created_at")
    else:
        tickets = Ticket.objects.filter(customer=request.user).order_by("-created_at")
    return render(request, "tickets/my_tickets.html", {"tickets": tickets})

# @staff_member_required
# def update_ticket(request, ticket_id):
#     ticket = get_object_or_404(Ticket, id=ticket_id)

#     if request.method == "POST":
#         form = AdminTicketForm(request.POST, instance=ticket)
#         if form.is_valid():
#             updated_ticket = form.save()

#             # Send email to customer when updated
#             send_mail(
#                 subject="Update on your support ticket",
#                 message=f"Hello {updated_ticket.customer.username},\n\n"
#                         f"Your ticket '{updated_ticket.subject}' has been updated.\n"
#                         f"Status: {updated_ticket.status}\n\n"
#                         f"Admin Notes: {updated_ticket.admin_notes or 'No notes'}\n\n"
#                         f"- Computer Planet",
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[updated_ticket.customer.email],
#                 fail_silently=False,
#             )

#             messages.success(request, "Ticket updated and customer notified.")
#             return redirect("tickets:admin_ticket_list")

#     else:
#         form = AdminTicketForm(instance=ticket)

#     return render(request, "tickets/update_ticket.html", {"form": form, "ticket": ticket})

@staff_member_required
def admin_ticket_list(request):
    tickets = Ticket.objects.all().order_by("-created_at")
    return render(request, "tickets/admin_ticket_list.html", {"tickets": tickets})

@staff_member_required  
def export_tickets_csv(request):
    tickets = Ticket.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tickets.csv"'

    writer = csv.writer(response)
    writer.writerow(['Ticket No', 'Subject', 'Status', 'Created'])
    for ticket in tickets:
        writer.writerow([ticket.ticket_no, ticket.subject, ticket.status, ticket.created_at.strftime('%Y-%m-%d %H:%M')])

    return response


def ticket_detail(request, pk):
    if request.user.is_staff:
        ticket = get_object_or_404(Ticket, pk=pk)
    else:
        ticket = get_object_or_404(Ticket, pk=pk, reported_by=request.user)
    
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})





def ticket_update(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketFormUpdate(request.POST, request.FILES, instance=ticket)
        notify_customer = request.POST.get("notify_customer")
        if form.is_valid():
            updated_ticket = form.save()

            if notify_customer:  # Send email to customer when updated
                ticket_url = request.build_absolute_uri(
    reverse('tickets:details_with_key', args=[ticket.pk, ticket.access_key])
)
                
            
                subject = f"Update on your support ticket #{updated_ticket.ticket_no}"

                # Plain text fallback
                text_body = (
                    f"Hello {updated_ticket.reported_by},\n\n"
                    f"Your ticket '{updated_ticket.subject}' has been updated.\n"
                    f"Status: {updated_ticket.get_status_display()}\n\n"
                    f"View your ticket here: {ticket_url}\n\n"
                    f"- Computer Planet"
                )

                # HTML version
                html_body = f"""
                    <p>Hello <strong>{updated_ticket.reported_by}</strong>,</p>
                    <p>Your support ticket <strong>#{updated_ticket.ticket_no}</strong>
                    (<em>{updated_ticket.subject}</em>) has been updated.</p>
                    <p><b>Status:</b> {updated_ticket.get_status_display()}</p>
                    <p><b>Admin Notes:</b> {updated_ticket.admin_notes}</p>
                    <p>
                        You can view your ticket here:
                        <a href="{ticket_url}" target="_blank">{ticket_url}</a>
                    </p>
                    <br>
                    <p>- <em>Computer Planet</em></p>
                """

                email = EmailMultiAlternatives(
                    subject=subject,
                    body=html_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[updated_ticket.customer.email],
                )
                email.attach_alternative(html_body, "text/html")
                email.send()

            messages.success(request, "Ticket updated successfully.")
            return redirect('tickets:details', pk=ticket.pk)
    else:
        form = TicketFormUpdate(instance=ticket)

    return render(request, 'tickets/ticket_update.html', {'form': form, 'ticket': ticket})

def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('tickets:my_tickets')
    return render(request, 'tickets/ticket_delete.html', {'ticket': ticket})


def ticket_detail_with_key(request, pk, access_key):
    ticket = get_object_or_404(Ticket, pk=pk, access_key=access_key)
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})
