from django_mako_plus import view_function, jscontext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

@view_function
def process_request(request):
        context = {}
        logout(request)
        return HttpResponseRedirect('/homepage/')
