from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import GPXPoint, GPXFile

from recursos.serializers import GPXPointSerializer


GPXPOINT_URL = reverse('recursos:gpxpoint-list')


def sample_user(email='test@londonappdev.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class PublicGPXPointsApiTests(TestCase):
    """Test the publically available GPXPoint API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(GPXPOINT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGPXPointsAPITests(TestCase):
    """Test GPXPoint can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_GPXPoint_list(self):
        """Test retrieving a list of GPXPoints"""
        gpxFile = GPXFile.objects.create(
            user=sample_user(email='test@londonappdevuu.com',
                             password='testpassuu'),
            nombre="Arakil",
        )
        GPXPoint.objects.create(
            user=self.user,
            nombre="ArakAra",
            gpx_fichero=gpxFile,
            geom=Point(5, 23)
        )
        GPXPoint.objects.create(
            user=self.user,
            nombre="Arak",
            gpx_fichero=gpxFile,
            geom=Point(5, 23)
        )

        res = self.client.get(GPXPOINT_URL)

        GPXPoints = GPXPoint.objects.all().order_by('-nombre')
        serializer = GPXPointSerializer(GPXPoints, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_GPXPoint_limited_to_user(self):
        """Test that only GPXPoint for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        gpxFile = GPXFile.objects.create(
            user=sample_user(email='test@londonappdevuu.com',
                             password='testpassuu'),
            nombre="Arakil",
        )
        GPXPoint.objects.create(
            user=user2,
            nombre="ArakArakñól",
            gpx_fichero=gpxFile,
            geom=Point(5, 23)
        )

        gpxpoint = GPXPoint.objects.create(user=self.user,
                                           nombre="ArakArakñól",
                                           gpx_fichero=gpxFile,
                                           geom=Point(5, 23))

        res = self.client.get(GPXPOINT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['nombre'], gpxpoint.nombre)

    def test_create_GPXPoint_successful(self):
        """Test creating a new GPXPoint"""
        gpxFile = GPXFile.objects.create(
            user=sample_user(email='test@londonappdevuu.com',
                             password='testpassuu'),
            nombre="Arakil",
        )
        payload = {'nombre': 'Arak', 'gpx_fichero': gpxFile.id,
                   'geom':
                   '{ "type": "Point", \
                   "coordinates": [ 5.000000, 23.000000 ] }'}
        self.client.post(GPXPOINT_URL, payload)

        exists = GPXPoint.objects.filter(
            user=self.user,
            nombre=payload['nombre'],
            geom=payload['geom']
        ).exists()
        self.assertTrue(exists)

    def test_create_GPXPoint_invalid(self):
        """Test creating invalid GPXPoint fails"""
        payload = {'nombre': 'Arak'}
        res = self.client.post(GPXPOINT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
