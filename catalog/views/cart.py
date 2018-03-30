from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless
from django import forms
from django.http import HttpResponseRedirect

@view_function
def process_request(request):

    print('*' * 80)
    cart = request.user.get_shopping_cart()
    cart.recalculate()
    line_items = cart.active_items()
    total_price = round(cart.total_price,2)
    # if cart.num_items() > 0:


    # Create form
    form = CheckoutForm(request)

    if form.is_valid():
        form.commit()
        # All data is clean at this point. Don't change the info.

        return HttpResponseRedirect('/catalog/checkout/')

    form.submit_text = ''
    context = {
        'form': form,
        'line_items': line_items,
        'total_price': total_price,
        }

    return request.dmp.render('cart.html', context)




class CheckoutForm(Formless):


    def init(self):
        '''Adds the fields for this form (called at end of __init__)'''
        # print('>' * 80)
        # self.fields['quantity'] = forms.CharField(label="Quantity",
        #     widget=forms.HiddenInput(),
        #     initial= None,
        #     required= False)

        pass


    def commit(self):
        # cart = self.request.user.get_shopping_cart()
        # product_in_cart = cart.get_item(product = self.product, create=True)
        # print(product_in_cart)
        # product_in_cart.quantity += int(self.cleaned_data.get('quantity'))
        # product_in_cart.save()
        #
        # # print(cart)
        # print(product_in_cart.quantity)
        pass
