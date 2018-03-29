from django.db import models
from cuser.models import AbstractCUser
from django.utils import timezone
from catalog import models as cmod
# from django.contrib.auth.models import AbstractUser

class User(AbstractCUser):
    address = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    zip = models.TextField(null=True, blank=True)

    def get_purchases(self):
        return ['Roku Ultimate 4', 'Skis', 'Computer']

    def get_shopping_cart(self):
        '''Get shopping cart. Create a new one if not already created '''
        cart = cmod.Order.objects.filter(status='cart', user_id = self.id).first()
        if cart is None:
            cart = cmod.Order()
            cart.user = self
            cart.save()

        return cart
