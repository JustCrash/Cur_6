from django.db.models import BooleanField
from django.forms import ModelForm, forms
from service.models import Client, Message, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ('last_name ', 'comment', 'owner')


class ClientModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ('last_name ', 'comment', 'owner')


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ("picture",)


class MessageModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ("picture",)


class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = ("message",)


class MailingModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = ("message",)