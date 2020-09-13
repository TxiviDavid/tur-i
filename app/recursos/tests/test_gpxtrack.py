from django.contrib.gis.geos import LineString, MultiLineString
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import GPXTrack, GPXFile

from recursos.serializers import GPXTrackSerializer


GPXTrack_URL = reverse('recursos:gpxtrack-list')


def sample_user(email='test@londonappdev.com',
                password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class PublicRestaurantesApiTests(TestCase):
    """Test the publically available GPXTrack API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(GPXTrack_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRestaurantesAPITests(TestCase):
    """Test GPXTrack can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_GPXTrack_list(self):
        """Test retrieving a list of GPXTracks"""
        gpxFile = GPXFile.objects.create(
            user=sample_user(email='test@londonappdevuu.com',
                             password='testpassuu'),
            nombre="Arakil",
        )
        ls1 = LineString((0, 0, 0), (1, 1, 1))
        ls2 = LineString((2, 2, 2), (3, 3, 3))
        mls = MultiLineString(ls1, ls2)
        GPXTrack.objects.create(
            user=self.user,
            nombre="ArakAra",
            tipo="Otros",
            gpx_fichero=gpxFile,
            geom=mls
        )
        ls1 = LineString((0, 3, 0), (1, 2, 1))
        ls2 = LineString((2, 1, 2), (2, 3, 3))
        mls = MultiLineString(ls1, ls2)
        GPXTrack.objects.create(
            user=self.user,
            nombre="Arak",
            tipo="Otros",
            gpx_fichero=gpxFile,
            geom=mls
        )

        res = self.client.get(GPXTrack_URL)

        GPXTracks = GPXTrack.objects.all().order_by('-nombre')
        serializer = GPXTrackSerializer(GPXTracks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_GPXTrack_limited_to_user(self):
        """Test that only GPXTrack for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        gpxFile = GPXFile.objects.create(
            user=sample_user(email='test@londonappdevuu.com',
                             password='testpassuu'),
            nombre="Arakil",
        )
        ls1 = LineString((0, 0, 0), (1, 1, 1))
        ls2 = LineString((2, 2, 2), (3, 3, 3))
        mls = MultiLineString(ls1, ls2)
        GPXTrack.objects.create(
            user=user2,
            nombre="ArakArakñól",
            tipo="Otros",
            gpx_fichero=gpxFile,
            geom=mls
        )

        gpxTrack = GPXTrack.objects.create(user=self.user,
                                           nombre="ArakArakñól",
                                           tipo="Otros",
                                           gpx_fichero=gpxFile,
                                           geom=mls)

        res = self.client.get(GPXTrack_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['nombre'], gpxTrack.nombre)

    def test_create_GPXTrack_successful(self):
        """Test creating a new GPXTrack"""
        gpxFile = GPXFile.objects.create(
            user=sample_user(email='test@londonappdevuu.com',
                             password='testpassuu'),
            nombre="Arakil",
        )
        payload = {'nombre': 'Arak', 'matricula': 'SL', 'observaciones': 'daf',
                   'gpx_fichero': gpxFile.id,
                   'geom': '{"type": "MultiLineString", "coordinates": \
                   [[[100.0, 0.0, 1],[101.0, 1.0, 6]], \
                   [[102.0, 2.0, 2],[103.0, 3.0, 1]]]}'}
        self.client.post(GPXTrack_URL, payload)

        exists = GPXTrack.objects.filter(
            user=self.user,
            nombre=payload['nombre'],
            geom=payload['geom']
        ).exists()
        self.assertTrue(exists)

    def test_create_restaurante_invalid(self):
        """Test creating invalid GPXTrack fails"""
        payload = {'nombre': 'Arak'}
        res = self.client.post(GPXTrack_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
