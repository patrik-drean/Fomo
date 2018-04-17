from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless
from django import forms
from django.http import HttpResponseRedirect
import traceback

@view_function
def process_request(request):

    cart = request.user.get_shopping_cart()
    cart.recalculate()
    total_price = round(cart.total_price, 2)



    # Create form
    form = CheckoutForm(request)

    if form.is_valid():
        form.commit()
        # All data is clean at this point. Don't change the info.

        return HttpResponseRedirect('/catalog/success/')

    context = {
        'form': form,
        'total_price': total_price,
        }

    return request.dmp.render('checkout.html', context)




class CheckoutForm(Formless):


    def init(self):
        '''Adds the fields for this form (called at end of __init__)'''
        self.fields['address'] = forms.CharField(label = 'Street Address')
        self.fields['state'] = forms.CharField(label = 'State')
        self.fields['country'] = forms.CharField(label = 'Country')
        self.fields['zip'] = forms.CharField(label = 'Zip Code')
        self.fields['stripeToken'] = forms.CharField(widget = forms.HiddenInput())


    def clean(self):
        cart = self.request.user.get_shopping_cart()
        try:
            token = self.cleaned_data.get('stripeToken')
            print(token)
            cart.finalize(token, int(round(cart.total_price, 2) * 100))
        except Exception as e:
            traceback.print_exc()
            raise forms.ValidationError('Payment failed: {}'.format(e))


    def commit(self):
        cart = self.request.user.get_shopping_cart()
        product_in_cart = cart.get_item(product = self.product, create=True)
        print(product_in_cart)
        product_in_cart.quantity += int(self.cleaned_data.get('quantity'))
        product_in_cart.save()

        # print(cart)
        print(product_in_cart.quantity)
        pass
