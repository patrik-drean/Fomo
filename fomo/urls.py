"""fomo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from catalog.views import search
from catalog import views
from django.urls import path

# router = routers.DefaultRouter()
# router.register(r'products', views.ProductViewSet)
# router.register(r'categories', views.CategoryViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    # the built-in Django administrator
    url(r'^admin/', admin.site.urls),

    # urls for any third-party apps go here
    # url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls'), namespace='rest_framework')),
    url(r'^catalog/search$', views.search.process_request, name='search'),
    # url(r'^catalog/search/(?P<id>\w{0,50})/$', views.search.process_request, name='search'),
    # path(r'^catalog/search/(?P<id>\w{0,50})/$', views.search.process_request, name='search'),
    path('catalog/search/<str:category_name>/<str:product_name>/<int:max_price>/<int:page>/', views.search.process_request,),

    # the DMP router - if DEFAULT_HOMEPAGE is set, this should be the last pattern (the wildcards match everything)
    url('', include('django_mako_plus.urls')),
]

# from django.conf.urls import url, include
# from rest_framework import routers
# from tutorial.quickstart import views
#
# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
#
# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]
