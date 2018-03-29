from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless
from django import forms

@view_function
def process_request(request, product:cmod.Product):

    # request.session['productid'] = product.id
    product = cmod.Product.objects.get(id = product.id)

    if product in request.last_five:
        request.last_five.remove(product)

    request.last_five.append(product)

    if len(request.last_five) > 6:
        request.last_five.pop(0)


    # Create form
    form = AddItemForm(request)
    form.submit_text = 'Add to Cart'
    if form.is_valid():
        form.commit()
        # All data is clean at this point. Don't change the info.

        return HttpResponseRedirect('/catalog/cart/')

    context = {
        'product': product,
        'form': form,
        }

    return request.dmp.render('detail.html', context)

# Put current view product into request.last_five

class AddItemForm(Formless):

    def init(self):
        '''Adds the fields for this form (called at end of __init__)'''
        pass

    def commit(self):
        pass
