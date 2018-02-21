from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.shortcuts import redirect
from catalog import models as cmod


@view_function
def process_request(request, deactivatedProduct:cmod.Product):

    context = {}
    # deactivatedProduct = cmod.Product.objects.get(id=productID)
    deactivatedProduct.Status = 'I'
    deactivatedProduct.save()

    return redirect('/manager/')
