from django import template


register = template.Library()


@register.filter()
def censor(value):
    new_text = value.replace('редиска', 'р******')
    new_text = new_text.replace('скуф', 'ск**')

    return new_text