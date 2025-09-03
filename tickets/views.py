from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Ticket
from .forms import TicketForm

class TicketListView(ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'

class MyTicketsView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/my_tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(customer=self.request.user)

class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('my_tickets')

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('my_tickets')

    def get_queryset(self):
        # Customers can only update their own tickets
        return Ticket.objects.filter(customer=self.request.user)

class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'tickets/ticket_confirm_delete.html'
    success_url = reverse_lazy('my_tickets')

    def get_queryset(self):
        return Ticket.objects.filter(customer=self.request.user)
