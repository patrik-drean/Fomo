from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod

@view_function
def process_request(request, categoryid = 0):
    if int(categoryid) > 0:
        category = cmod.Category.objects.get(id = categoryid)
        products = cmod.Product.objects.all().filter(Category_id = category.id).filter(Status = 'A')
    else:
        category = None
        products = cmod.Product.objects.all().filter(Status = 'A')

    totalPageCount = int(len(products) / 6) + 1
    categories = cmod.Category.objects.all()
    context = { 'categories': categories,
                'category': category,
                jscontext('categoryid'): categoryid,
                jscontext('pageid'): 0,
                jscontext('totalPageCount'): totalPageCount,}

    return request.dmp.render('index.html', context)

@view_function
def products(request, categoryid = 0, pageid:int = 1):

    # Load the products based off of category
    if int(categoryid) > 0:
        category = cmod.Category.objects.get(id = categoryid)
        products = cmod.Product.objects.all().filter(Category_id = category.id).filter(Status = 'A')
    else:
        category = None
        products = cmod.Product.objects.all().filter(Status = 'A')

    # Divide the products up to show total pages and only display 6 products
    totalPageCount = int(len(products) / 6) + 1
    sixProducts = []

    if pageid == totalPageCount:
        maxProductPosition = len(products)
        productPosition = (pageid - 1) * 6
    else:
        maxProductPosition = pageid * 6
        productPosition = (pageid - 1) * 6

    while(productPosition < maxProductPosition):
        if products[productPosition] is not None:
            sixProducts.append(products[productPosition])
        productPosition += 1

    categories = cmod.Category.objects.all()
    context = {'sixProducts': sixProducts,
                'categories': categories,
                'category': category,
                'totalPageCount': totalPageCount,
                'pageid': pageid,
                jscontext('categoryid'): categoryid,
                jscontext('pageid'): pageid,
                jscontext('totalPageCount'): totalPageCount,}

    return request.dmp.render('index.products.html', context)
