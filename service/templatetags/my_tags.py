from django import template

register = template.Library()


@register.filter()
def my_media(val):
    if val:
        return f"/media/{val}"
    else:
        return "Тут могла быть картинка, но ее не загрузили..."
