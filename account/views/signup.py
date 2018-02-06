from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext

@view_function
def process_request(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/homepage/index/')
    else:
        form =SignupForm()

    context = {
        "form": form,
    }
    return request.dmp_render('signup.html', context)


class SignupForm(forms.Form):
    favorite_ice_cream = forms.CharField(label = "Choclate is my friend")
    renewal_date = forms.CharField(label="Renewal")
