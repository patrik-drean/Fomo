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
    return request.dmp_render('create.html', context)


class CreateForm(Formless):

    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop('product_id')
        super(CreateForm, self).__init__(*args, **kwargs)
        '''This is defaulted, but now i can edit by using the above 2 lines'''

    def init(self):
        '''Adds the fields for this form (called at end of __init__)'''

        # Grab the existing product or create a new product
        if(self.product_id > -1):
            product = cmod.Product.objects.get(id = self.product_id)
        else:
            product = cmod.Product()
            product.Category = cmod.Category.objects.all().first()
            self.fields['Type'] = forms.ChoiceField(label = 'Product Type',
                                                    choices = product.TYPE_CHOICES,
                                                    )

        self.fields['Name'] = forms.CharField(  label="Name",
                                                initial = product.Name,)
        self.fields['Description'] = forms.CharField(
                                                    label="Description",
                                                    initial = product.Description,
                                                    )
        self.fields['Category'] = forms.ModelChoiceField(label="Category",
                                                    queryset = cmod.Category.objects.all(),
                                                    initial = product.Category
                                                    )
        self.fields['Status'] = forms.ChoiceField(
        choices=product.STATUS_CHOICES,
        )
        self.fields['Price'] = forms.CharField(label="Price", initial = product.Price)

        # Bulk Fields
        if hasattr(product, 'TITLE'):
            if product.TITLE == 'Bulk':
                self.fields['Quantity'] = forms.CharField(label="Quantity", initial = product.Quantity,required = False)
                self.fields['ReorderTrigger'] = forms.CharField(label="Reorder Trigger", initial = product.ReorderTrigger,required = False)
                self.fields['ReorderQuantity'] = forms.CharField(label="Reorder Quantity", initial = product.ReorderQuantity, required = False)
            else:
                self.fields['Quantity'] = forms.CharField(label="Quantity",required = False)
                self.fields['ReorderTrigger'] = forms.CharField(label="Reorder Trigger",required = False)
                self.fields['ReorderQuantity'] = forms.CharField(label="Reorder Quantity",required = False)

            # Individual fields
            if product.TITLE == 'Individual' or product.TITLE == 'Rental':
                self.fields['ItemID'] = forms.CharField(label="ItemID", initial = product.ItemID, required = False)
            else:
                self.fields['ItemID'] = forms.CharField(label="ItemID",required = False)

            # Rental fields
            if product.TITLE == 'Rental':
                self.fields['MaxRental'] = forms.CharField(label="Max Rental Days", initial = product.MaxRental, required = False)
                self.fields['RetireDate'] = forms.DateField(label='Rental Date', initial = product.RetireDate, required = False)
            else:
                self.fields['MaxRental'] = forms.CharField(label="Max Rental Days",required = False)
                self.fields['RetireDate'] = forms.DateField(label="Rental Date",required = False)
        else:
            self.fields['Quantity'] = forms.CharField(label="Quantity",required = False)
            self.fields['ReorderTrigger'] = forms.CharField(label="Reorder Trigger",required = False)
            self.fields['ReorderQuantity'] = forms.CharField(label="Reorder Quantity",required = False)
            self.fields['ItemID'] = forms.CharField(label="ItemID",required = False)
            self.fields['MaxRental'] = forms.CharField(label="Max Rental Days",required = False)
            self.fields['RetireDate'] = forms.DateField(label="Rental Date",required = False)

        self.submit_text = 'Submit'

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if len(pwd) < 8:
            raise forms.ValidationError('Password must be at least 8 characters')
        if not re.search('[0-9]+', pwd):
            raise forms.ValidationError('Your password must include at least one number.')
        return pwd

    def clean_email(self):
        # Grab user from database with email. If a user comes back, throw exception
        email = self.cleaned_data.get('email')
        users = amod.User.objects.filter(email = email)
        if users:
            raise forms.ValidationError('Email already exists in database')
        return email

    def clean(self):
        p1 = self.cleaned_data.get("password")
        p2 = self.cleaned_data.get("password2")
        if p1 != p2:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data

    def commit(self):
        user = amod.User()
        user.email = self.cleaned_data.get("email")
        user.set_password(self.cleaned_data.get("password"))
        user.address = self.cleaned_data.get("address")
        user.state = self.cleaned_data.get("state")
        user.zip = self.cleaned_data.get("zip")

        user.save()

        user = authenticate(email = user.email, password = self.cleaned_data.get("password"))
        login(self.request, user)
