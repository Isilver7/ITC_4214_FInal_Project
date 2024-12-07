from django import template

register = template.Library()

# Example of a simple custom filter
@register.filter
def add_class(value, css_class):
    return value.as_widget(attrs={'class': css_class})
