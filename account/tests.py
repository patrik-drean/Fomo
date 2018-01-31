from django.test import TestCase
from account import models as amod
from datetime import datetime
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType

class UserClassTestCase(TestCase):

    def setUp(self):
        self.user = amod.User()
        self.user.first_name = 'Lisa'
        self.user.last_name = 'Simpson'
        self.user.email = 'lisa@simpsons.com'
        self.user.set_password('password')
        # self.user.birthdate = '1965-02-04'
        self.user.address = '243 spring road'
        self.user.state = 'Utah'
        self.user.zip = '22123'

        #Save to database
        self.user.save()

    def test_load_save(self):
        '''Test creating, saving, and reloading a user'''

        user2 = amod.User.objects.get(email = self.user.email)

        self.assertEqual(self.user.first_name, user2.first_name)
        self.assertEqual(self.user.last_name, user2.last_name)
        self.assertEqual(self.user.email, user2.email)
        self.assertTrue(user2.check_password('password'))
        self.assertEqual(self.user.address, user2.address)
        self.assertEqual(self.user.state, user2.state)
        self.assertEqual(self.user.zip, user2.zip)

    def test_adding_groups(self):
        '''Test adding a few groups'''
        # group 1 with 1 permission
        group = Group(name="Test")
        group.save()
        ct = ContentType.objects.get_for_model(amod.User)
        permission = Permission.objects.create(codename ='can_view',
                                                name ='Can view',
                                                content_type = ct)
        group.permissions.add(permission)
        group.save()
        self.user.groups.add(group)

        # group 2 with 1 permission
        group = Group(name="Test2")
        group.save()
        ct = ContentType.objects.get_for_model(amod.User)
        permission = Permission.objects.create(codename ='can_edit',
                                                name ='Can edit',
                                                content_type = ct)
        group.permissions.add(permission)
        group.save()
        self.user.groups.add(group)

        self.user.save()

        permission = Permission.objects.get(codename = 'can_edit')
        print(permission)

        # Check permission is assigned to the user
        test = self.user.has_perm('account.can_edit')
        self.assertTrue(test)
        test2 = self.user.has_perm('account.can_view')
        self.assertTrue(test2)

    # def test_adding_permissions(self):
    #     '''Test adding a few permissions'''
         # permission = Permission.objects.get(name='account | user | can add user')
         # self.user.user_permissions.add(permission)

    def test_login(request):
        '''Test to login a user succesfully'''
        username = 'lisa@simpsons.com'
        password = 'password'
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # login(request, user)
                print(user.first_name)
            else:
                print('no')
        else:
            print('no')

    def test_logoff(self):
        '''Test adding a few permissions'''


    def test_field_changes(self):
        '''Test changing user attributes'''
        updatedUser = amod.User.objects.get(email = self.user.email)
        updatedUser.first_name = 'Tommy'
        updatedUser.last_name = 'Trucky'

        updatedUser.save()

        updatedUser2 = amod.User.objects.get(email = updatedUser.email)
        self.assertEqual(updatedUser.first_name, updatedUser2.first_name)
        self.assertEqual(updatedUser.last_name, updatedUser2.last_name)




    # Django Example
    # def test_animals_can_speak(self):
    #     """Animals that can speak are correctly identified"""
    #     lion = Animal.objects.get(name="lion")
    #     cat = Animal.objects.get(name="cat")
    #     self.assertEqual(lion.speak(), 'The lion says "roar"')
    #     self.assertEqual(cat.speak(), 'The cat says "meow"')
