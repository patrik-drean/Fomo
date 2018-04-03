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
from catalog.views import views
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', ])
def process_request(request, category_name = '', product_name = '', max_price = 999999, page = 1):
# def process_request(request, category_name, product_name, max_price = 999999, page = 1):
    print('*' * 80)
    print(category_name)
    products = cmod.Product.objects.all().order_by("Category","Name")
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

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
