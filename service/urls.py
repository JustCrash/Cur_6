from django.urls import path
from service.apps import ServiceConfig
from service.views import (ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView,
                           ClientDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView,
                           MessageDeleteView, ContactsView,
                           MailingView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView)
app_name = ServiceConfig.name


urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('contacts/', ContactsView.as_view(), name="contact_list"),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/create/', ClientCreateView.as_view(), name='client_form'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_form'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailing/', MailingView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_form'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
]