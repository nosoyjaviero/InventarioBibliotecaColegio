from django import template

register = template.Library()

@register.filter
def add_id(field, css_id):
    return field.as_widget(attrs={'id': css_id})