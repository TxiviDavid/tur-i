from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import PuntoInteres

from recursos.serializers import PuntoInteresSerializer


PUNTOSINTERES_URL = reverse('recursos:puntosInteres-list')


class PublicTagsApiTests(TestCase):
    """Test the publicly available puntosInteres API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving tags"""
        res = self.client.get(PUNTOSINTERES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user puntosInteres API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_puntosInteres(self):
        """Test retrieving puntosInteres"""
        PuntoInteres.objects.create(user=self.user, nombre='Vegan')
        PuntoInteres.objects.create(user=self.user, nombre='Dessert')

        res = self.client.get(PUNTOSINTERES_URL)

        pois = PuntoInteres.objects.all().order_by('-nombre')
        serializer = PuntoInteresSerializer(pois, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_PuntoInteres_limited_to_user(self):
        """Test that PuntoInteres returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        PuntoInteres.objects.create(user=user2, nombre='Fruity')
        poi = PuntoInteres.objects.create(user=self.user,
                                          nombre='Comfort Food')

        res = self.client.get(PUNTOSINTERES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['nombre'], poi.nombre)

    def test_create_tag_successful(self):
        """Test creating a new puntosInteres"""
        payload = {'nombre': 'Simple'}
        self.client.post(PUNTOSINTERES_URL, payload)

        exists = PuntoInteres.objects.filter(
            user=self.user,
            nombre=payload['nombre']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new puntosInteres with invalid payload"""
        payload = {'nombre': ''}
        res = self.client.post(PUNTOSINTERES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
