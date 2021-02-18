from django.urls import path
from .views import ticket_review_create_and_list_view , TicketDeleteView, TicketUpdateView

app_name = 'Tickets'

urlpatterns = [
    path('', ticket_review_create_and_list_view, name='main-ticket-view'),
    # path('liked/', like_unlike_post, name='like-ticket-view'),
    path('<pk>/delete/', TicketDeleteView.as_view(), name='Ticket-delete'),
    path('<pk>/update/', TicketUpdateView.as_view(), name='Ticket-update'),
]