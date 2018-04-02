from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless
from django import forms
from django.http import HttpResponseRedirect
import traceback
import json
from rest_framework import viewsets
from catalog.views.serializers import ProductSerializer, CategorySerializer



@view_function
def process_request(request, category, product, max_price, page = 1):


    return
#
#     result = cmod.Product.objects.all()
#     serializer_class = ProductSerializer
#
#     # json_list = []
#     #
#     # for product in result:
#     #     json_list.append(product.toJSON)
#
#     return result
