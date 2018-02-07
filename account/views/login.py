from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from formlib import Formless
import re

@view_function
def process_request(request):
    form = SignupForm(request)
    if form.is_valid():
        # All data is clean at this point. Don't change the info.
        return HttpResponseRedirect('/account/index/')

    context = {
        "form": form,
    }
    return request.dmp_render('signup.html', context)


class LoginForm(Formless):


    def init(self):
        '''Adds the fields for this form (called at end of __init__)'''
        self.fields['email'] = forms.CharField(label="Email")
        self.fields['password'] = forms.CharField(
                                                    label="Password",
                                                    widget=forms.PasswordInput
                                                    )


    def clean(self):
        p1 = self.cleaned_data.get("password")
        p2 = self.cleaned_data.get("password2")
        if p1 != p2:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data
