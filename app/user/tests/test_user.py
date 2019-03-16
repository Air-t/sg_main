from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

CREATE_USER_URL = reverse('user:signup')


# def create_user(**params):
#     return get_user_model().objects.create_user(**params)


class UserTestCase(TestCase):
    """Tests user model"""

    def setUp(self):
        self.client = Client()
        self.username = 'marian'
        self.email = 'test@gmail.com'
        self.password = 'marian1234'


    def test_user_is_created(self):
        """Test user is created successfully"""
        user = get_user_model().objects.create_user(username=self.username,
                                                    email=self.email,
                                                    password=self.password
                                                    )

        user = get_user_model().objects.get(username=self.data.username)
        self.assertIsNotNone(user)

    def test_user_is_created_with_unique_username(self):
        """Test user is created with unique username"""
        user = get_user_model().objects.create_user(**self.data)
        user.save()
        user2 = get_user_model().objects.create_user(**self.data)
        user2.save()
        self.assertIsNone(user2)


    # def test_user_is_created_with_success(self):
    #     """Test if user is created successfully"""
    #     data = {
    #         'username': 'marian',
    #         'email': 'test@gmail.com',
    #         'password': 'test1234',
    #     }
    #     response = self.client.post(CREATE_USER_URL, data)
    #     user = get_user_model().objects.get(**response.context['user'])
    #     self.assertIsNone(user)

    # def test_unique_username(self):
    #     """Test if username is unique in database"""
    #     data = {
    #         'username': 'marian',
    #         'email': 'test@gmail.com',
    #         'password': 'test1234',
    #     }
    #     self.client.post(CREATE_USER_URL, data)
    #     response = self.client.post(CREATE_USER_URL, data)
    #     self.assertEqual(response.status_code, 200)

    # def test_create_user_with_email_successful(self):
    #     """Test crating a new user with an email is successful"""
    #
    #     email = "test@gmail.com"
    #     password = "test1234"
    #     user = get_user_model().objects.create_user(
    #         email=email,
    #         password=password
    #     )
    #
    #     self.assertEqual(user.email, email)
    #     self.assertTrue(user.check_password(password))
