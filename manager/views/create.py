from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from formlib import Formless
import re
from catalog import models as cmod
from django.contrib.auth import authenticate, login

@view_function
def process_request(request, product:cmod.Product = None):

    # Determine if we're creating a new product or if we're editing one
    if(product is not None):
        productID = product.id
    else:
        productID = -1

    form = CreateForm(request, product_id = productID)
    if form.is_valid():
        form.commit()
        # All data is clean at this point. Don't change the info.

        return HttpResponseRedirect('/manager/')

    context = {
        "form": form,
    }
    return request.dmp.render('create.html', context)


class CreateForm(Formless):

    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop('product_id')
        # Grab the existing product or create a new product
        if(self.product_id > -1):
            self.product = cmod.Product.objects.get(id = self.product_id)
        else:
            self.product = cmod.Product()
            self.product.Category = cmod.Category.objects.all().first()

        super(CreateForm, self).__init__(*args, **kwargs)
        '''This is defaulted, but now i can edit by using the above 2 lines'''

    def init(self):
        '''Adds the fields for this form (called at end of __init__)'''

        if (self.product_id < 0):
            self.fields['Type'] = forms.ChoiceField(label = 'Product Type',
                                                choices = self.product.TYPE_CHOICES,
                                                )

        else:
            self.fields['Type'] = forms.CharField(initial = self.product.TITLE,
                                                widget = forms.HiddenInput(),
                                                )

        self.fields['Name'] = forms.CharField(  label="Name",
                                                initial = self.product.Name,)
        self.fields['Description'] = forms.CharField(
                                                    label="Description",
                                                    initial = self.product.Description,
                                                    )
        self.fields['Category'] = forms.ModelChoiceField(label="Category",
                                                    queryset = cmod.Category.objects.all(),
                                                    initial = self.product.Category
                                                    )
        self.fields['Status'] = forms.ChoiceField(
        choices=self.product.STATUS_CHOICES,
        )
        self.fields['Price'] = forms.CharField(label="Price", initial = self.product.Price)

        # Bulk Fields
        if hasattr(self.product, 'TITLE'):
            if self.product.TITLE == 'BulkProduct':
                self.fields['Quantity'] = forms.CharField(label="Quantity", initial = self.product.Quantity,required = False)
                self.fields['ReorderTrigger'] = forms.CharField(label="Reorder Trigger", initial = self.product.ReorderTrigger,required = False)
                self.fields['ReorderQuantity'] = forms.CharField(label="Reorder Quantity", initial = self.product.ReorderQuantity, required = False)
            else:
                self.fields['Quantity'] = forms.CharField(label="Quantity",required = False)
                self.fields['ReorderTrigger'] = forms.CharField(label="Reorder Trigger",required = False)
                self.fields['ReorderQuantity'] = forms.CharField(label="Reorder Quantity",required = False)

            # Individual fields
            if self.product.TITLE == 'IndividualProduct' or self.product.TITLE == 'RentalProduct':
                self.fields['ItemID'] = forms.CharField(label="ItemID", initial = self.product.ItemID, required = False)
            else:
                self.fields['ItemID'] = forms.CharField(label="ItemID",required = False)
            # Rental fields
            if self.product.TITLE == 'RentalProduct':
                self.fields['MaxRental'] = forms.CharField(label="Max Rental Days", initial = self.product.MaxRental, required = False)
                self.fields['RetireDate'] = forms.DateField(label='Retire Date (yyyy-mm-dd)', initial = self.product.RetireDate, required = False)
            else:
                self.fields['MaxRental'] = forms.CharField(label="Max Rental Days",required = False)
                self.fields['RetireDate'] = forms.DateField(label="Retire Date (yyyy-mm-dd)",required = False)
        else:
            self.fields['Quantity'] = forms.CharField(label="Quantity",required = False)
            self.fields['ReorderTrigger'] = forms.CharField(label="Reorder Trigger",required = False)
            self.fields['ReorderQuantity'] = forms.CharField(label="Reorder Quantity",required = False)
            self.fields['ItemID'] = forms.CharField(label="ItemID",required = False)
            self.fields['MaxRental'] = forms.CharField(label="Max Rental Days",required = False)
            self.fields['RetireDate'] = forms.DateField(label="Retire Date (yyyy-mm-dd)",required = False)

        self.submit_text = 'Submit'


    def clean(self):
        ''' Make sure unique fields are filled in based on product type chosen'''
        type = self.cleaned_data.get('Type')
        if type == 'BulkProduct':
            qty = self.cleaned_data.get('Quantity')
            trigger = self.cleaned_data.get('ReorderTrigger')
            reorderQty = self.cleaned_data.get('ReorderQuantity')

            if qty == '':
                raise forms.ValidationError('Quantity is a required field')
            if trigger == '':
                raise forms.ValidationError('Reorder Trigger is a required field')
            if reorderQty == '':
                raise forms.ValidationError('Reorder quantity is a required field')

        # Individual Fields
        if type == 'IndividualProduct' or type == 'RentalProduct':
            itemID = self.cleaned_data.get('ItemID')

            if itemID == '':
                raise forms.ValidationError('Item ID is a required field')

        # Rental Fields
        if type == 'RentalProduct':
            maxRental = self.cleaned_data.get('MaxRental')
            rentalDate = self.cleaned_data.get('RetireDate')

            if maxRental == '':
                raise forms.ValidationError('Max Rental is a required field')
            if rentalDate == None:
                raise forms.ValidationError('Retire Date is a required field')

        return self.cleaned_data

    def commit(self):
        ''' Save the product if it's new. Get the product and change it if it's edit.'''

        # Get all the generic data
        type = self.cleaned_data.get('Type')
        category = cmod.Category.objects.get(Name = self.cleaned_data.get('Category'))
        name = self.cleaned_data.get('Name')
        description = self.cleaned_data.get('Description')
        price = self.cleaned_data.get('Price')
        status = self.cleaned_data.get('Status')
        qty = self.cleaned_data.get('Quantity')
        reorderTrigger = self.cleaned_data.get('ReorderTrigger')
        reorderQuantity = self.cleaned_data.get('ReorderQuantity')
        itemID = self.cleaned_data.get('ItemID')
        maxRental = self.cleaned_data.get('MaxRental')
        retireDate = self.cleaned_data.get('RetireDate')

        # Create the product
        if type == 'BulkProduct':
            if self.product_id < 0:
                bProduct = cmod.BulkProduct()
            else:
                bProduct = self.product
            bProduct.new_object( name, description, category, price, status)
            bProduct.Quantity = qty
            bProduct.ReorderTrigger = reorderTrigger
            bProduct.ReorderQuantity = reorderQuantity

            bProduct.save()

        if type == 'IndividualProduct':
            if self.product_id < 0:
                iProduct = cmod.IndividualProduct()
            else:
                iProduct = self.product
            iProduct.new_object( name, description, category, price, status)
            iProduct.ItemID = itemID

            iProduct.save()

        if type == 'RentalProduct':
            if self.product_id < 0:
                rProduct = cmod.RentalProduct()
            else:
                rProduct = self.product
            rProduct.new_object( name, description, category, price, status)
            rProduct.ItemID = itemID
            rProduct.MaxRental = maxRental
            rProduct.RetireDate = retireDate

            rProduct.save()
