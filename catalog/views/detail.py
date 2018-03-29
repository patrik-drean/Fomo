from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless
from django import forms
from django.http import HttpResponseRedirect

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
    form = AddItemForm(request, product_id = product.id)
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

    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop('product_id')
        self.product = cmod.Product.objects.get(id = self.product_id)

        super(AddItemForm, self).__init__(*args, **kwargs)
        '''This is defaulted, but now i can edit by using the above 2 lines'''

    def init(self):
        '''Adds the fields for this form (called at end of __init__)'''
        # print('>' * 80)
        self.fields['quantity'] = forms.CharField(label="Quantity",
            widget=forms.HiddenInput(),
            initial= None,
            required= False)

        pass

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')



        if qty != '':
            if int(qty) < 1:
                raise forms.ValidationError('Enter at least 1 for quantity')

            total_db_qty = cmod.Product.objects.get(id = self.product.id).Quantity
            line_item = cmod.OrderItem.objects.filter(
                order=self.request.user.get_shopping_cart(),
                product=self.product).first()
            if line_item is not None:
                total_qty = int(qty) + line_item.quantity
            else:
                total_qty = int(qty)
            if total_qty > total_db_qty:
                raise forms.ValidationError('Insufficient quantity')



        print('>' * 80)
        print(qty)
        print(self.request.user.get_shopping_cart())
        print(self.product)
        print(line_item)
        print(total_db_qty)

        return qty



    def commit(self):
        cart = self.request.user.get_shopping_cart()
        cart.get_item(product = self.product, create=True)
        print(cart)
        print(cart.get_item(product=self.product))
