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

    # Filter by category
    if category_name != 'na':
        products = cmod.Product.objects.filter(Category__Name__icontains = category_name)
    else:
        products = cmod.Product.objects.all()

    # Filter by product
    if product_name != 'na':
        products = products.filter(Name__icontains = product_name)
    else:
        pass

    # Filter by price
    products = products.filter(Price__lte = max_price)

    # Order by category and product name
    products = products.order_by("Category__Name","Name")

    # Filter by page
    totalPageCount = int(len(products) / 6) + 1

    sixProducts = []

    if page == totalPageCount:
        maxProductPosition = len(products)
        productPosition = (page - 1) * 6
    else:
        maxProductPosition = page * 6
        productPosition = (page - 1) * 6

    while(productPosition < maxProductPosition):
        if products[productPosition] is not None:
            sixProducts.append(products[productPosition])
        productPosition += 1

    # Output
    serializer = ProductSerializer(sixProducts, many=True)
    return Response(serializer.data)
