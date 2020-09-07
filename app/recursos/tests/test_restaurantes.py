from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Restaurante

from recursos.serializers import RestauranteSerializer


RESTAURANTES_URL = reverse('recursos:restaurante-list')


class PublicRestaurantesApiTests(TestCase):
    """Test the publically available Restaurantes API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(RESTAURANTES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRestaurantesAPITests(TestCase):
    """Test Restaurantes can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_restaurante_list(self):
        """Test retrieving a list of Restaurantes"""
        Restaurante.objects.create(user=self.user, nombre='kale')
        Restaurante.objects.create(user=self.user, nombre='salt')

        res = self.client.get(RESTAURANTES_URL)

        restaurants = Restaurante.objects.all().order_by('-nombre')
        serializer = RestauranteSerializer(restaurants, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_restaurantes_limited_to_user(self):
        """Test that only restaurantes for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        Restaurante.objects.create(user=user2, nombre='Vinegar')

        restaurante = Restaurante.objects.create(user=self.user,
                                                 nombre='tumeric')

        res = self.client.get(RESTAURANTES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['nombre'], restaurante.nombre)

    def test_create_restaurante_successful(self):
        """Test creating a new restaurante"""
        payload = {'nombre': 'piku1'}
        self.client.post(RESTAURANTES_URL, payload)

        exists = Restaurante.objects.filter(
            user=self.user,
            nombre=payload['nombre']
        ).exists()
        self.assertTrue(exists)

    def test_create_restaurante_invalid(self):
        """Test creating invalid restaurante fails"""
        payload = {'nombre': ''}
        res = self.client.post(RESTAURANTES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
