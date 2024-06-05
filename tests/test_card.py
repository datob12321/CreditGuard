from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


# class CardTests(APITestCase):
#
#     def test_card(self):
#         card_data_1 = {'ccv': 534, 'card_number': 5495830412738493}
#         card_data_2 = {'ccv': 1023, 'card_number': 7893746583947584}
#         card_data_3 = {'ccv': 908, 'card_number': 4565456545654}
#
#         response_1 = self.client.post('/cards/', data=card_data_1)
#         self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
