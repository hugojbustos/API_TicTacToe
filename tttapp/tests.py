from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Game


class TicTacToeAPITestCase(APITestCase):
    def test_create_game(self):
        url = reverse('create_game')
        data = {
            "players": [
                {"name": "me"},
                {"name": "other"}
            ],
            "starting_player": "me"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Game.objects.get().players.count(), 2)
