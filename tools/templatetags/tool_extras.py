from django import template

register = template.Library()


@register.filter(name="three_digits_currency")
def three_digits_currency(value: int):
    return f"{value:,}"
