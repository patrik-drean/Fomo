from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required

# @permission_required('can_create',  login_url='/account/login/')
@view_function
def process_request(request):

    cart = request.user.get_shopping_cart()
    cart.recalculate()
    line_items = cart.active_items()
    total_price = round(cart.total_price,2)
    # if cart.num_items() > 0:



    context = {
        'line_items': line_items,
        'total_price': total_price,
        }

    return request.dmp.render('cart.html', context)
