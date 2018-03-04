from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod

@view_function
def process_request(request, categoryid = 0):
    if int(categoryid) > 0:
        category = cmod.Category.objects.get(id = categoryid)
        products = cmod.Product.objects.all().filter(Category_id = category.id, Status = 'A')
    else:
        category = None
        products = cmod.Product.objects.all()
    categories = cmod.Category.objects.all()
    productCount = int(len(products) / 6) + 1
    context = {'products': products,
                'categories': categories,
                'category': category,
                'productCount': productCount}
    return request.dmp.render('index.html', context)

@view_function
def products(request, categoryid = 0):
    if int(categoryid) > 0:
        category = cmod.Category.objects.get(id = categoryid)
        products = cmod.Product.objects.all().filter(Category_id = category.id, Status = 'A')
    else:
        category = None
        products = cmod.Product.objects.all()
    categories = cmod.Category.objects.all()
    productCount = int(len(products) / 6) + 1
    context = {'products': products,
                'categories': categories,
                'category': category,
                'productCount': productCount}
    return request.dmp.render('index.products.html', context)
