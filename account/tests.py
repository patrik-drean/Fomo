from django.test import TestCase
from account import models as amod
from datetime import datetime
from django.contrib.auth.models import Group


class UserClassTestCase(TestCase):

    def setUp(self):
        self.user = amod.User()
        self.user.first_name = 'Lisa'
        self.user.last_name = 'Simpson'
        self.user.email = 'lisa@simpsons.com'
        self.user.set_password('password')
        self.user.birthdate = '1965-02-04'
        self.user.address = '243 spring road'
        self.user.state = 'Utah'
        self.user.zip = '22123'

    def test_load_save(self):
        '''Test creating, saving, and reloading a user'''

        #Save to database
        self.user.save()

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
        # my_group = Group.objects.get(name='Test')
        # my_group.user_set.add(self.user)
        print(Group.objects.all())






    # Django Example
    # def test_animals_can_speak(self):
    #     """Animals that can speak are correctly identified"""
    #     lion = Animal.objects.get(name="lion")
    #     cat = Animal.objects.get(name="cat")
    #     self.assertEqual(lion.speak(), 'The lion says "roar"')
    #     self.assertEqual(cat.speak(), 'The cat says "meow"')
