from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from formlib import Formless
from django.contrib.auth import authenticate, login
import re
from ldap3 import Server, Connection
from simplejson import loads
from account import models as amod
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

@view_function
def process_request(request, product_id = None, qty = None):
    form = LoginForm(request)
    if form.is_valid():
        form.commit()
        if product_id is None and qty is None:
            return HttpResponseRedirect('/homepage/')
        else:
            form.commit_cart(product_id, qty)
            return HttpResponseRedirect('/catalog/cart')
    context = {
        "form": form,
    }

    return request.dmp.render('login.html', context)


class LoginForm(Formless):


    def init(self):
        '''Adds the fields for this form (called at end of __init__)'''
        self.fields['email'] = forms.CharField(label="Email")
        self.fields['password'] = forms.CharField(
                                                    label="Password",
                                                    widget=forms.PasswordInput
                                                    )
        self.submit_text = 'Login'


    def clean(self):
        user_email = self.cleaned_data.get('email')
        user_password = self.cleaned_data.get('password')

        # Check if user is in Active Directory

        # user_email = 'bclark@musical-family.me'
        # user_password = 'Server!'


        # ad_check = None
        server = Server('musical-family.me')
        conn = Connection(server, user='MUSICAL-FAMILY\\Administrator', password='IS5Server!')
        search_base = 'cn=Users,dc=musical-family,dc=local'
        search_filter = '(mail=' + user_email + ')'
        conn.bind()

        # See if username is in Active Directory
        if conn.search(search_base,search_filter,attributes='sAMAccountName'):
            name = 'MUSICAL-FAMILY\\' + loads(conn.response_to_json())['entries'][0]['attributes']['sAMAccountName']
            conn = Connection(server,user=name,password=user_password)

            # Authenticate user if password is correct
            if conn.bind():
                # Authenticate user if in database
                self.user = authenticate(
                                        email = user_email,
                                        password = user_password,
                                        )
                # Create user in database if authentication failed
                if self.user is None:
                    self.user = amod.User()
                    self.user.email = user_email
                    self.user.set_password(user_password)

                    # Add permission
                    ct = ContentType.objects.get_for_model(amod.User)
                    permission1 = Permission.objects.get(codename ='can_create')

                    self.user.save()
                    self.user.user_permissions.add(permission1)
                    self.user.save()

                    self.user = authenticate(
                                            email = user_email,
                                            password = user_password,
                                            )

            # Raise exception if user password is incorrect
            else:
                raise forms.ValidationError('Invalid Active Directory Password')

        # Authenticate if user is not in Active Directory
        else:
            self.user = authenticate(
                                    email = user_email,
                                    password = user_password,
                                    )
            if self.user is None:
                raise forms.ValidationError('Invalid email or password')

    def commit(self):
        #authenticate away
        login(self.request, self.user)

    def commit_cart(self, product_id, qty):
        cart = self.request.user.get_shopping_cart()
        if qty == '':
            qty = 0
        else:
            qty = int(qty)
            qty = qty - 1


        # Grab the current product selected and create it the cart
        product_in_cart = cart.get_item(id=product_id, create=True)

        # Add the quantity to what the line item already has in the cart
        product_in_cart.quantity += qty

        # Save updated line item
        product_in_cart.save()
