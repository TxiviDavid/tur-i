from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.contrib.gis.geos import Point, LineString, MultiLineString

from rest_framework import status
from rest_framework.test import APIClient

from core.models import TrackPoint, GPXTrack, GPXFile

from recursos.serializers import TrackPointSerializer


TRACKPOINT_URL = reverse('recursos:trackpoint-list')


def sample_user(email='test@londonappdev.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class PublicTrackPointsApiTests(TestCase):
    """Test the publically available TrackPoint API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(TRACKPOINT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTrackPointsAPITests(TestCase):
    """Test TrackPoint can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_TrackPoint_list(self):
        """Test retrieving a list of TrackPoint"""
        gpxFile = GPXFile.objects.create(
            user=sample_user(email='test@londonappdevuu.com',
                             password='testpassuu'),
            nombre="Arakil",
        )
        ls1 = LineString((0, 3, 0), (1, 2, 1))
        ls2 = LineString((2, 1, 2), (2, 3, 3))
        mls = MultiLineString(ls1, ls2)
        gpxTrack = GPXTrack.objects.create(user=self.user,
                                           nombre="Arak",
                                           tipo="Otros",
                                           gpx_fichero=gpxFile,
                                           geom=mls)

        TrackPoint.objects.create(user=self.user,
                                  nombre='rtth',
                                  sendero=gpxTrack,
                                  geom=Point(5, 23))

        TrackPoint.objects.create(user=self.user,
                                  nombre='jg',
                                  sendero=gpxTrack,
                                  geom=Point(5, 23))

        res = self.client.get(TRACKPOINT_URL)

        TrackPoints = TrackPoint.objects.all().order_by('-nombre')
        serializer = TrackPointSerializer(TrackPoints, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_TrackPoints_limited_to_user(self):
        """Test that only TrackPoints for authenticated user are returned"""
        gpxFile = GPXFile.objects.create(
            user=sample_user(email='test@londonappdevuu.com',
                             password='testpassuu'),
            nombre="Arakil",
        )
        ls1 = LineString((0, 3, 0), (1, 2, 1))
        ls2 = LineString((2, 1, 2), (2, 3, 3))
        mls = MultiLineString(ls1, ls2)
        gpxTrack = GPXTrack.objects.create(user=self.user,
                                           nombre="Arak",
                                           tipo="Otros",
                                           gpx_fichero=gpxFile,
                                           geom=mls)

        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        TrackPoint.objects.create(user=user2,
                                  nombre='uii',
                                  sendero=gpxTrack,
                                  geom=Point(5, 23))

        trackpoint = TrackPoint.objects.create(user=self.user,
                                               nombre='iuu',
                                               sendero=gpxTrack,
                                               geom=Point(5, 23))

        res = self.client.get(TRACKPOINT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['nombre'], trackpoint.nombre)

    def test_create_TrackPoint_successful(self):
        """Test creating a new TrackPoint"""
        gpxFile = GPXFile.objects.create(
            user=sample_user(email='test@londonappdevuu.com',
                             password='testpassuu'),
            nombre="Arakil",
        )
        ls1 = LineString((0, 3, 0), (1, 2, 1))
        ls2 = LineString((2, 1, 2), (2, 3, 3))
        mls = MultiLineString(ls1, ls2)
        gpxTrack = GPXTrack.objects.create(user=self.user,
                                           nombre="Arak",
                                           tipo="Otros",
                                           gpx_fichero=gpxFile,
                                           geom=mls)

        payload = {'nombre': 'A', 'sendero': gpxTrack.id, 'geom':
                   '{"type": "Point", \
                   "coordinates": [ 5.000000, 23.000000 ] }'}
        self.client.post(TRACKPOINT_URL, payload)
        exists = TrackPoint.objects.filter(
            nombre=payload['nombre'],
            geom=payload['geom']
        ).exists()
        self.assertTrue(exists)

    def test_create_TrackPoint_invalid(self):
        """Test creating invalid TrackPoint fails"""
        payload = {'nombre': ''}
        res = self.client.post(TRACKPOINT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
