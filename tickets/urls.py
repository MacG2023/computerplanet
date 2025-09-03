from django.urls import path
from . import views

app_name = "tickets"

urlpatterns = [
    path("create/", views.create_ticket, name="tickets"),
    

     path('details/<int:pk>/', views.ticket_detail, name='details'),
    path('update/<int:pk>/', views.ticket_update, name='update_ticket'),
    path('delete/<int:pk>/', views.ticket_delete, name='delete'),
  
    path("my/", views.my_tickets, name="tickets_list"),
    path("my/", views.my_tickets, name="my_tickets"),

    path("tickets/<int:pk>/<uuid:access_key>/", views.ticket_detail_with_key, name="details_with_key"),

    

   
    path("create/", views.create_ticket, name="create_ticket"),
    path("admin/list/", views.admin_ticket_list, name="admin_ticket_list"),
    # path("admin/update/<int:ticket_id>/", views.update_ticket, name="update_ticket"),
    path('tickets/export-csv/', views.export_tickets_csv, name='export_csv'),
   
]
