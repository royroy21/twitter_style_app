# Python Imports
import datetime

# Django Imports
from django.test import TestCase
from django.contrib.auth.models import User
from twitter_style_app_1.models import UserStatus
from twitter_style_app_1.models import UserExtended
from django.test import Client


class TwitterStyleApp1Tests(TestCase):
    def setUp(self):
        """
        Test set ups.
        """
        # create test user
        user_object = User.objects.create_user(username='harry1',
                                               first_name='Harry',
                                               last_name='Gibbon',
                                               email='hgibbon@gmail.com',
                                               password='big fat gibbon')
        user_object.save()
        user_extended_object = UserExtended(user=user_object)
        user_extended_object.save()

        # create test user first status post
        date_of_first_post = datetime.datetime.strptime("2014-12-01", "%Y-%m-%d")
        user_status_1 = UserStatus(user=user_extended_object,
                                   status="Harry's first status post",
                                   date_created=date_of_first_post)
        user_status_1.save()

        # create test user second status post
        date_of_second_post = datetime.datetime.strptime("2014-12-01", "%Y-%m-%d")
        user_status_2 = UserStatus(user=user_extended_object,
                                   status="Harry's second status post",
                                   date_created=date_of_second_post)
        user_status_2.save()

        # create test user third status post
        user_status_3 = UserStatus(user=user_extended_object,
                                   status="Harry's third status post")
        user_status_3.save()

    def create_user_to_test_with(self):
        """
        Creates a user to use with the following tests.
        """
        user_object = User.objects.create_user(username='roy1',
                                               first_name='Roy',
                                               last_name='Hanley',
                                               email='rhanley8@gmail.com',
                                               password='small fat gibbon')
        user_object.save()
        user_extended_object = UserExtended(user=user_object)
        user_extended_object.save()
        return

    def test_user_registration(self):
        """
        Tests new user registration.
        """
        post_data = {'username': 'roy1',
                     'first_name': 'Roy',
                     'last_name': 'Hanley',
                     'email': 'royhanley8@gmail.com',
                     'password': 'small fat gibbon'}
        response = Client().post('/register_new_user/', post_data)

        # tests response
        self.assertEqual('user roy1 successfully created' in response.content, True)

        # tests if User object has successfully been created
        self.assertEqual(User.objects.filter(username='roy1').exists(), True)

        # test if UserExtended has successfully been created and correctly linked to User object
        self.assertEqual(UserExtended.objects.filter(user__username='roy1').exists(), True)
        return

    def test_user_login(self):
        """
        Tests user authentication (login / logout).
        """
        # create user
        post_data = {'username': 'roy1',
                     'first_name': 'Roy',
                     'last_name': 'Hanley',
                     'email': 'royhanley8@gmail.com',
                     'password': 'small fat gibbon'}
        Client().post('/register_new_user/', post_data)

        # login with test user 'roy1'
        post_data = {'username': 'roy1',
                     'password': 'small fat gibbon'}
        response = Client().post('/user_login/', post_data)

        # tests response
        self.assertEqual('user roy1 successfully logged in' in response.content, True)
        return

    def test_user_logout(self):
        # create user and log in a user to test with
        self.create_user_to_test_with()
        client = Client()
        client.login(username='roy1', password='small fat gibbon')

        # log user out
        response = client.get('/user_logout/')

        # tests response
        self.assertEqual('log out successful' in response.content, True)
        return

    def test_posting_of_status_updates(self):
        """
        Tests posting of status updates (only authenticated users can post status updates).
        """
        # create user and log in a user to test with
        self.create_user_to_test_with()

        # post data
        post_data = {'user_id': User.objects.get(username='roy1').id,
                     'status': 'my first status post'}

        # tests posting a status without user authenticated first
        response = Client().post('/new_status/', post_data)

        # tests response
        self.assertEqual('user roy1 successfully created new status' in response.content, False)

        # tests that new status has not been created
        self.assertEqual(UserStatus.objects.filter(status='my first status post',
                                                   user__id=User.objects.get(username='roy1').id).exists(),
                         False)

        # tests posting a status
        client = Client()
        client.login(username='roy1', password='small fat gibbon')
        response = client.post('/new_status/', post_data)

        # tests response
        self.assertEqual('user roy1 successfully created new status' in response.content, True)

        # tests that new status has not been created
        self.assertEqual(UserStatus.objects.filter(status='my first status post',
                                                   user__id=User.objects.get(username='roy1').id).exists(),
                         True)
        return

    def test_ability_to_follow_other_users(self):
        """
        Ability to follow other users (only if authenticated).
        """
        # create user and log in a user to test with
        self.create_user_to_test_with()

        # tests following user without user authenticated first
        response = Client().get('/follow_user/%d/%d/' % (User.objects.get(username='roy1').id,
                                                         User.objects.get(username='harry1').id))

        # tests response
        self.assertEqual('user roy1 successfully following harry1' in response.content, False)

        # tests that user roy1 is not following harry1 yet
        followed_user_id = User.objects.get(username='harry1').id
        self.assertEqual(UserExtended.objects.filter(user__username='roy1',
                                                     users_following__id=followed_user_id).exists(),
                         False)

        # tests following user with user authenticated
        client = Client()
        client.login(username='roy1', password='small fat gibbon')
        response = client.get('/follow_user/%d/%d/' % (User.objects.get(username='roy1').id,
                                                       User.objects.get(username='harry1').id))

        # tests response
        self.assertEqual('user roy1 successfully following harry1' in response.content, True)

        # tests that user roy1 is not following harry1 yet
        followed_user_id = User.objects.get(username='harry1').id
        self.assertEqual(UserExtended.objects.filter(user__username='roy1',
                                                     users_following__id=followed_user_id).exists(),
                         True)
        return

    def test_view_a_users_public_time_line(self):
        """
        View a users public time line.
        """
        # create user and log in a user to test with
        self.create_user_to_test_with()

        # tests viewing a user's public time line without user authenticated first
        response = Client().get('/view_time_line/%d/' % User.objects.get(username='harry1').id)

        # tests response
        for status in ["Harry's first status post", "Harry's second status post", "Harry's third status post"]:
            self.assertEqual(status in response.content, False)

        # tests viewing a user's public time line with the user logged in
        client = Client()
        client.login(username='roy1', password='small fat gibbon')
        response = client.get('/view_time_line/%d/' % User.objects.get(username='harry1').id)

        # tests response
        for status in ["Harry's first status post", "Harry's second status post", "Harry's third status post"]:
            self.assertEqual(status in response.content, True)
        return