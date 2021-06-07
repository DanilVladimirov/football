from django import template
from club.models import *

register = template.Library()


@register.filter(name='is_in_cart')
def have_item(request, item_id):
    has_item = False
    cart = request.session.get('cart', {})

    if request.POST:
        for item in cart:
            if int(request.POST.get('item_id')) == item.get('item'):
                del cart[cart.index(item)]
    return has_item
