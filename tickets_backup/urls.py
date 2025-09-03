from django.urls import path
from .views import (
    TicketListView, MyTicketsView, TicketDetailView,
    TicketCreateView, TicketUpdateView, TicketDeleteView
)

urlpatterns = [
    path('', TicketListView.as_view(), name='tickets'),             # admin/support view
    path('my/', MyTicketsView.as_view(), name='my_tickets'),        # logged-in user's tickets
    path('create/', TicketCreateView.as_view(), name='ticket_create'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('<int:pk>/update/', TicketUpdateView.as_view(), name='ticket_update'),
    path('<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket_delete'),
]
