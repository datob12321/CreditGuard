from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient
from django.contrib.auth.models import User
from .models import Card
from django.urls import reverse
from .serializers import MySerializer

user = User.objects.get(username="dato")
class CardTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='password12321')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.card1 = {'ccv': 5354, 'card_number': 5495830412738493}

    def test_card(self):
        card_data_1 = {'ccv': 5354, 'card_number': 5495830412738493}
        card_data_2 = {'ccv': 106, 'card_number': 7894746484947884}
        card_data_3 = {'ccv': 900, 'card_number': 456545654565443}
        card_data_4 = {'ccv': 998, 'card_number': 45454545454545498}

        response_1 = self.client.get('/cards/', data=card_data_1)
        response_2 = self.client.post('/cards/', data=card_data_2, format='json')
        response_3 = self.client.post('/cards/', data=card_data_3, format='json')
        response_4 = self.client.post('/cards/', data=card_data_4, format='json')
        self.assertEqual(response_4.data['message']['non_field_errors'][0], 'it must be between 100 and 900!')
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(Card.objects.count(), 1)

        self.assertEqual(Card.objects.get().is_valid, True)
        self.assertEqual(response_3.data['message']['non_field_errors'][0], "it must has 16 characters!")

    def test_card_validation(self):
        self.client.get('/cards/', format='json', data=self.card1)
        self.client.post('/cards/', data=self.card1, format='json')
        self.assertEqual(Card.objects.count(), 1)


