from django.test import TestCase
from account import models as amod
from datetime import datetime
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, RequestFactory

class UserClassTestCase(TestCase):

    # Load up fixtures
    fixtures = ['data.yaml']

    def setUp(self):

        # Load up the user
        self.user = amod.User()
        self.user.first_name = 'Lisa'
        self.user.last_name = 'Simpson'
        self.user.email = 'lisa@simpsons.com'
        self.user.set_password('password')
        self.user.address = '243 spring road'
        self.user.state = 'Utah'
        self.user.zip = '22123'

        # Save to database
        self.user.save()

    def test_load_save(self):
        '''Test creating, saving, and reloading a user'''

        # Load user from database
        user2 = amod.User.objects.get(email = self.user.email)

        # Compare the 2 user objects together
        self.assertEqual(self.user.first_name, user2.first_name)
        self.assertEqual(self.user.last_name, user2.last_name)
        self.assertEqual(self.user.email, user2.email)
        self.assertEqual(self.user.password, user2.password)
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
        permission.save()
        group.permissions.add(permission)
        group.save()

        # add group to user
        self.user.groups.add(group)

        # group 2 with 1 permission
        group = Group(name="Test2")
        group.save()
        ct = ContentType.objects.get_for_model(amod.User)
        permission = Permission.objects.create(codename ='can_edit',
                                                name ='Can edit',
                                                content_type = ct)
        permission.save()
        group.permissions.add(permission)
        group.save()

        #add group to user
        self.user.groups.add(group)
        self.user.save()

        # Check groups are assigned to the user
        user_in_group = Group.objects.get(name="Test").user_set.get(email = self.user.email)
        self.assertTrue(user_in_group, self.user)

        user_in_group2 = Group.objects.get(name="Test2").user_set.get(email = self.user.email)
        self.assertTrue(user_in_group2, self.user)

        # Check permissions are assigned to the user
        test1 = self.user.has_perm('account.can_edit')
        self.assertTrue(test1)
        test2 = self.user.has_perm('account.can_view')
        self.assertTrue(test2)

    def test_adding_permissions(self):
         '''Test adding a few permissions directly to the user'''
         ct = ContentType.objects.get_for_model(amod.User)
         permission1 = Permission.objects.create(codename ='can_delete',
                                                 name ='Can delete',
                                                 content_type = ct)

         permission2 = Permission.objects.create(codename ='can_create',
                                                 name ='Can create',
                                                 content_type = ct)
         self.user.user_permissions.add(permission1, permission2)

         # Check permissions are assigned to the user
         test1 = self.user.has_perm('account.can_delete')
         self.assertTrue(test1)
         test2 = self.user.has_perm('account.can_create')
         self.assertTrue(test2)

    # def test_login(self):
    #     '''Test to login a user succesfully'''
    #
    #     # Authenticate
    #     username = 'lisa@simpsons.com'
    #     password = 'password'
    #     user = authenticate(username=username, password=password)
    #
    #     # Create fake request
    #     response = self.client.get("account/index")
    #     request = response.wsgi_request
    #
    #     # Login user
    #     if user is not None:
    #             login(request, user)
    #
    #     # Test if user was logged in
    #     self.assertFalse(user.is_anonymous)
    #
    #
    # def test_logoff(self):
    #     '''Test logging off a user'''

    def test_check_password(self):
        ''' Check password '''
        self.assertTrue(self.user.check_password('password'))

    def test_field_changes(self):
        '''Test changing user attributes'''

        # Grab user and make changes
        updatedUser = amod.User.objects.get(email = self.user.email)
        updatedUser.first_name = 'Tommy'
        updatedUser.last_name = 'Trucky'

        updatedUser.save()

        # Grab the updated user and test it's changed
        updatedUser2 = amod.User.objects.get(email = updatedUser.email)
        self.assertEqual(updatedUser.first_name, updatedUser2.first_name)
        self.assertEqual(updatedUser.last_name, updatedUser2.last_name)
