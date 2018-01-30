from django.db import models
from cuser.models import AbstractCUser
# from django.contrib.auth.models import AbstractUser

class User(AbstractCUser):
    # first_name = models.TextField(null=True, blank = True)
    # last_name = models.TextField(null=True, blank = True)
    birthdate = models.DateTimeField(null=True, blank = True)
    address = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    zip = models.TextField(null=True, blank=True)

    def get_purchases(self):
        return ['Roku Ultimate 4', 'Skis', 'Computer']
