from django import template
from django.core.handlers.wsgi import WSGIRequest
from django.utils.safestring import SafeString, mark_safe

from menu.models import MenuItem

# To be a valid tag library, the module must contain a module-level
# variable named 'register'
register = template.Library()

RelTable = dict[str, list[str]]

@register.simple_tag
def draw_menu(request: WSGIRequest):
    """Returns html snippet that contains tree based menu view."""

    rel_table, cur_menuitem = _menu_handler(request)
    tree: str = ''

    # Initialize variable to store previous menu item value
    prev_menuitem: MenuItem | None = None
    while cur_menuitem:
        # Build tree from active menu item
        # Initialize subsequent tree variable to store temporary part of the tree
        sub_tree: str = ''
        # Iterate through current menu item's childs
        for child in rel_table[cur_menuitem.title]:
            sub_tree += _li_tag(_a_tag(child.title, child.path))
            if prev_menuitem and child == prev_menuitem:
                sub_tree += tree
        sub_tree = _ul_tag(sub_tree)
        tree = sub_tree

        # Store title for next iteration
        prev_menuitem = cur_menuitem
        cur_menuitem = cur_menuitem.parent

    sub_tree = ''
    for child in rel_table['root']:
        sub_tree += _li_tag(_a_tag(child.title, child.path))
        if prev_menuitem and child == prev_menuitem:
            sub_tree += tree
    sub_tree = _ul_tag(sub_tree)
    tree = sub_tree

    return mark_safe(tree)

def _li_tag(s: str) -> str:
    return '<li>' + s + '</li>'

def _ul_tag(s: str) -> str:
    return '<ul>' + s + '</ul>'

def _a_tag(s: str, href: str = '') -> str:
    return f'<a href="{href}">{s}</a>'

def _menu_handler(request: WSGIRequest) -> tuple[RelTable, MenuItem | None]:
    """Returns relationship table between menu items."""

    menu = MenuItem.objects.all()
    rel_table: RelTable = {'root': []}
    active_menuitem: MenuItem | None = None
    for item in menu:
        if item.path == request.path:
            active_menuitem = item

        if not item.parent:
            rel_table['root'].append(item)
            continue

        elif item.parent.title not in rel_table:
            rel_table[item.parent.title] = []
        rel_table[item.parent.title].append(item)

    if active_menuitem and active_menuitem.title not in rel_table:
        rel_table[active_menuitem.title] = []

    return (rel_table, active_menuitem)
