from django import template
from django.utils.html import format_html
from main.models import MenuItem

register = template.Library()

@register.simple_tag
def draw_menu():
    items = MenuItem.objects.all()
    menu_html = "<ul>"
    for item in items:
        menu_html += f'<li><a href="{item.url}">{item.name}</a></li>'
    menu_html += "</ul>"
    return format_html(menu_html)
