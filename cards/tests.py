from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Card
from .views import is_valid_card
import time
import random
import multiprocessing


class CardTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password12321')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.card1 = {'ccv': 536, 'card_number': 5495830412738493, 'title': 'title 1'}
        self.card2 = {'ccv': 1064, 'card_number': 7894746484947884, 'title': 'title 2'}
        self.card3 = {'ccv': 900, 'card_number': 4565456545654437, 'title': 'title 3'}
        self.card4 = {'ccv': 798, 'card_number': 45454545454545498, 'title': 'title 4'}

    def test_ccv_valid(self):
        response_2 = self.client.post('/cards/', data=self.card2, format='json')
        self.assertEqual(response_2.data['message']['non_field_errors'][0], 'it must be between 100 and 900!')

    def test_card_number_valid(self):
        response_4 = self.client.post('/cards/', data=self.card4, format='json')
        self.assertEqual(response_4.data['message']['non_field_errors'][0], 'it must has 16 digit characters!')

    def test_valid_card(self):
        self.client.post('/cards/', data=self.card1)
        is_valid = is_valid_card(self.card1['card_number'], self.card1['ccv'])
        self.assertEqual(Card.objects.get().is_valid, is_valid)

    def test_invalid_card(self):
        resp = self.client.post('/cards/', data=self.card3)
        self.assertEqual(Card.objects.get().is_valid, False)
        self.assertEqual(resp.data['new card']['is_valid'], False)

    def post_card(self):
        for i in range(50):
            ccv = random.randint(100, 900)
            card_numb = ''
            for j in range(16):
                card_numb += str(random.randint(1, 9))
            card_number = int(card_numb)
            data = {'ccv': ccv, 'card_number': card_number, 'title': f'title{i + 1}'}
            response = self.client.post('/cards/', data=data, format='json')
            self.assertEqual(response.data['new card']['is_valid'], is_valid_card(card_number, ccv))

    def test_speed(self):
        current_time = time.time()

        multiprocessing.process.BaseProcess(self.post_card())
        multiprocessing.process.BaseProcess(self.post_card())

        end_time = time.time()
        duration = end_time - current_time
        self.assertLess(duration, 140)
