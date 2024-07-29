from django import template
from django.urls import reverse
from menu.models import Menu, MenuItem
from menu.templatetags.url_filters import get_url

register = template.Library()

@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path

    try:
        menu = Menu.objects.prefetch_related('items').get(name=menu_name)
    except Menu.DoesNotExist:
        return {'menu_items': []}

    def build_tree(items, parent=None):
        tree = []
        for item in items:
            if item.parent == parent:
                tree.append({
                    'item': item,
                    'children': build_tree(items, item),
                    'active': current_url == get_url(item),
                    'expanded': False,
                })
        return tree

    menu_items = menu.items.all()
    menu_tree = build_tree(menu_items)

    def mark_active(items):
        for item in items:
            if item['active']:
                item['expanded'] = True
                return True
            if mark_active(item['children']):
                item['expanded'] = True
                return True
        return False

    mark_active(menu_tree)

    return {'menu_items': menu_tree}
