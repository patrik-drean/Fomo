from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from formlib import Formless
import re
from account import models as amod
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

@view_function
def process_request(request):
    form = SignupForm(request)
    if form.is_valid():
        form.commit()
        # All data is clean at this point. Don't change the info.

        return HttpResponseRedirect('/homepage/')

    context = {
        "form": form,
    }
    return request.dmp.render('signup.html', context)


class SignupForm(Formless):


    def init(self):
        '''Adds the fields for this form (called at end of __init__)'''
        self.fields['email'] = forms.CharField(label="Email")
        self.fields['password'] = forms.CharField(
                                                    label="Password",
                                                    widget=forms.PasswordInput
                                                    )
        self.fields['password2'] = forms.CharField(
                                                    label="Confirm Password",
                                                    widget=forms.PasswordInput
                                                    )

        self.fields['address'] = forms.CharField(label="Address")
        self.fields['state'] = forms.CharField(label="State")
        self.fields['zip'] = forms.CharField(label="Zip Code")
        self.submit_text = 'Sign Up'

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

        # Add permission
        ct = ContentType.objects.get_for_model(amod.User)
        # permission1 = Permission.objects.get(codename ='can_create')

        user.save()
        # user.user_permissions.add(permission1)
        # user.save()

        user = authenticate(email = user.email, password = self.cleaned_data.get("password"))
        login(self.request, user)
