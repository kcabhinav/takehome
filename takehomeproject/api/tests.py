from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import CustomUser
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError


class RegisterViewTest(APITestCase):
    def setUp(self):
        # Create a sample referral code for testing
        self.referral_user = CustomUser.objects.create(
            email='referral@example.com',
            name='Referral User',
            mobile_number='1234567890',
            city='Test City',
            password='Password123'
        )

        # Referral code of the created user
        self.referral_code = self.referral_user.referral_code

        # Define the registration endpoint
        self.url = reverse('register')

    def test_register_success(self):
        # Test valid registration
        data = {
            'email': 'testuser@example.com',
            'name': 'Test User',
            'mobile_number': '9876543210',
            'city': 'New York',
            'password': 'Password123',
            'confirm_password': 'Password123',
            'referrer_code': self.referral_code  # Providing a valid referral code
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('referral_code', response.data)
        self.assertEqual(len(response.data['referral_code']), 8)  # Ensure referral code is 8 characters

    def test_register_without_referral_code(self):
        # Test registration without providing a referral code
        data = {
            'email': 'testuser2@example.com',
            'name': 'Test User 2',
            'mobile_number': '9876543211',
            'city': 'Los Angeles',
            'password': 'Password123',
            'confirm_password': 'Password123'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_invalid_email(self):
        # Test registration with invalid email
        data = {
            'email': 'invalid-email',
            'name': 'Invalid Email User',
            'mobile_number': '9876543212',
            'city': 'Chicago',
            'password': 'Password123',
            'confirm_password': 'Password123'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_email_already_exists(self):
        # Test registration with an already existing email
        data = {
            'email': 'referral@example.com',
            'name': 'Another User',
            'mobile_number': '9876543213',
            'city': 'Miami',
            'password': 'Password123',
            'confirm_password': 'Password123'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_passwords_dont_match(self):
        # Test registration with mismatched passwords
        data = {
            'email': 'testuser3@example.com',
            'name': 'Test User 3',
            'mobile_number': '9876543214',
            'city': 'Houston',
            'password': 'Password123',
            'confirm_password': 'DifferentPassword'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirm_password', response.data)

    def test_register_invalid_referral_code(self):
        # Test registration with an invalid referral code
        data = {
            'email': 'testuser4@example.com',
            'name': 'Test User 4',
            'mobile_number': '9876543215',
            'city': 'Boston',
            'password': 'Password123',
            'confirm_password': 'Password123',
            'referrer_code': 'INVALIDCODE'  # Invalid referral code
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('referrer_code', response.data)


class LoginViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create(
            email='testuser@example.com',
            name='Test User',
            mobile_number='9876543216',
            city='San Francisco',
            password='Password123'
        )

        # Define the login endpoint
        self.url = reverse('login')

    def test_login_success(self):
        # Test valid login
        data = {
            'email': 'testuser@example.com',
            'password': 'Password123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('user_id', response.data)
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_login_invalid_email(self):
        # Test login with invalid email
        data = {
            'email': 'invalid@example.com',
            'password': 'Password123'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_invalid_password(self):
        # Test login with incorrect password
        data = {
            'email': 'testuser@example.com',
            'password': 'WrongPassword'
        }

        import pdb; pdb.set_trace() 
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReferralListViewTest(APITestCase):

    def setUp(self):
        # Create a user with referrals
        self.referrer = CustomUser.objects.create(
            email='referrer@example.com',
            name='Referrer User',
            mobile_number='9876543217',
            city='Dallas',
            password='Password123'
        )

        # Create a couple of users who will be referrals
        self.referral_1 = CustomUser.objects.create(
            email='referral1@example.com',
            name='Referral User 1',
            mobile_number='9876543218',
            city='Austin',
            password='Password123',
            referred_by=self.referrer
        )

        self.referral_2 = CustomUser.objects.create(
            email='referral2@example.com',
            name='Referral User 2',
            mobile_number='9876543219',
            city='Austin',
            password='Password123',
            referred_by=self.referrer
        )

        # Define the referral list endpoint
        self.url = reverse('referrals', kwargs={'user_id': self.referrer.id})

    def test_get_referrals_success(self):
        # Test getting referrals of a user
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # There should be two referrals
        self.assertEqual(response.data[0]['email'], 'referral1@example.com')
        self.assertEqual(response.data[1]['email'], 'referral2@example.com')

    def test_get_referrals_no_referrals(self):
        # Test getting referrals when there are no referrals
        new_user = CustomUser.objects.create(
            email='newuser@example.com',
            name='New User',
            mobile_number='9876543220',
            city='New York',
            password='Password123'
        )
        response = self.client.get(reverse('referrals', kwargs={'user_id': new_user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No referrals

    def test_get_referrals_user_not_found(self):
        # Test getting referrals for a non-existing user
        response = self.client.get(reverse('referrals', kwargs={'user_id': 999999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
