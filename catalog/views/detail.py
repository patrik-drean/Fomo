from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod

@view_function
def process_request(request, product:cmod.Product):

    # request.session['productid'] = product.id
    product = cmod.Product.objects.get(id = product.id)

    if product in request.last_five:
        request.last_five.remove(product)

    request.last_five.append(product)

    if len(request.last_five) > 6:
        request.last_five.pop(0)

    context = {
        'product': product,
        }

    return request.dmp.render('detail.html', context)

# Put current view product into request.last_five
