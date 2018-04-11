from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod

@permission_required('account.admin',  login_url='/account/login/')
@view_function
def process_request(request):
    # Load up fixtures
    fixtures = ['testing_data.yaml']

    activeProducts = cmod.Product.objects.filter(Status = 'A')
    context = {
    'activeProducts': activeProducts,
    }

    return request.dmp.render('index.html', context)
