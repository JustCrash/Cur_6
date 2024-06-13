from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory, ModelForm

from service.forms import MailingModeratorForm, MessageModeratorForm, MessageForm, MailingForm, ClientForm, \
    StyleFormMixin
from service.models import Client, Message, Mailing, Attempt, Contacts
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    fields = ['email', 'first_name', 'last_name']
    template_name = 'service/client_list.html'
    extra_context = {'title': 'Клиенты'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    success_url = reverse_lazy('service:client_list')

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    fields = ['email', 'first_name', 'last_name']
    template_name = 'service/client_detail.html'
    success_url = reverse_lazy('service:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_item = self.get_object()
        context['title'] = client_item.first_name
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['email', 'first_name', 'last_name']
    template_name = 'service/client_form.html'
    success_url = reverse_lazy('service:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание клиента'
        return context

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Client.objects.all()


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ['email', 'first_name', 'last_name']
    template_name = 'service/client_form.html'
    success_url = reverse_lazy('service:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_item = self.get_object()
        context['title'] = client_item.first_name
        return context


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    fields = ['email', 'first_name', 'last_name', 'comment']
    template_name = 'service/client_confirm_delete.html'
    success_url = reverse_lazy('service:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_item = self.get_object()
        context['title'] = client_item.first_name
        return context


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    fields = ['subject', 'text', 'picture']
    template_name = 'service/message_list.html'
    extra_context = {'title': 'Напишите сообщение'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    fields = ['subject', 'text', 'picture']
    template_name = 'service/message_detail.html'
    success_url = reverse_lazy('service:message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message_item = self.get_object()
        context['title'] = message_item.subject
        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['subject', 'text', 'picture']
    template_name = 'service/message_form.html'
    success_url = reverse_lazy('service:message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание сообщения'
        return context

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ['subject', 'text', 'picture']
    template_name = 'service/message_form.html'
    success_url = reverse_lazy('service:message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message_item = self.get_object()
        context['title'] = message_item.subject
        return context

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MessageForm
        if user.groups.filter(name='Manager').exists():
            return MessageModeratorForm
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    fields = ['subject', 'text', 'picture']
    template_name = 'service/message_confirm_delete.html'
    success_url = reverse_lazy('service:message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message_item = self.get_object()
        context['title'] = message_item.subject
        return context


class MailingView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mailing
    fields = ['time_sending', 'time_end', 'periodicity', 'status', 'clients']
    template_name = 'service/mailing_list.html'
    extra_context = {'title': 'Рассылка'}
    permission_required = 'service.view_maling'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    fields = ['time_sending', 'time_end', 'periodicity', 'status', 'clients']
    template_name = 'service/mailing_detail.html'
    success_url = reverse_lazy('service:mailing_form')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_item = self.get_object()
        context['title'] = mailing_item.time_sending
        return context


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    fields = ['time_sending', 'time_end', 'periodicity', 'status', 'clients']
    template_name = 'service/mailing_form.html'
    success_url = reverse_lazy('service:mailing_list')
    permission_required = 'service.add_maling'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание рассылки'
        return context

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Mailing.objects.all()


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    fields = ['time_sending', 'time_end', 'periodicity','status', 'clients']
    template_name = 'service/mailing_form.html'
    permission_required = 'service.change_maling'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_item = self.get_object()
        context['title'] = mailing_item.time_sending
        return context

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        if user.groups.filter(name='Manager').exists():
            return MailingModeratorForm
        raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    fields = ['time_sending', 'time_end', 'periodicity','status', 'clients']
    template_name = 'service/mailing_confirm_delete.html'
    success_url = reverse_lazy('service:mailing_list')
    permission_required = 'service.delete_maling'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_item = self.get_object()
        context['title'] = mailing_item.time_sending
        return context


class AttemptView(LoginRequiredMixin, ListView):
    model = Attempt
    fields = ['status']
    template_name = 'service/attempt_list.html'
    extra_context = {'title': 'Попытки'}


class ContactsView(LoginRequiredMixin, ListView):
    model = Contacts
    fields = ['name', 'phone', 'email']
    extra_context = {'title': 'Контакты'}
    template_name = 'service/contact_list.html'