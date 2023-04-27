from django import template

from menu.models import MenuItem

# To be a valid tag library, the module must contain a module-level
# variable named 'register'
register = template.Library()

@register.simple_tag
def draw_menu(request):
    menu = MenuItem.objects.all()
    return menu
