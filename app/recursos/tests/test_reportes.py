from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Reporte

from recursos.serializers import ReporteSerializer


REPORTES_URL = reverse('recursos:reporte-list')


class PublicReportesApiTests(TestCase):
    """Test the publically available Reportes API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(REPORTES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReportesAPITests(TestCase):
    """Test Reportes can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_reporte_list(self):
        """Test retrieving a list of Reportes"""
        Reporte.objects.create(user=self.user, signo=2, tipo=2, detalle=2)
        Reporte.objects.create(user=self.user, signo=2, tipo=2, detalle=2)

        res = self.client.get(REPORTES_URL)

        reportes = Reporte.objects.all().order_by('-id')
        serializer = ReporteSerializer(reportes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_reportes_limited_to_user(self):
        """Test that only reportes for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        Reporte.objects.create(user=user2, signo=2, tipo=2, detalle=2)

        reporte = Reporte.objects.create(user=self.user,
                                         signo=2, tipo=2, detalle=2)

        res = self.client.get(REPORTES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['signo'], reporte.signo)

    def test_create_reporte_successful(self):
        """Test creating a new reporte"""
        payload = {'signo': 2, 'tipo': 2, 'detalle': 2}
        self.client.post(REPORTES_URL, payload)

        exists = Reporte.objects.filter(
            user=self.user,
            signo=payload['signo'],
            tipo=payload['tipo'],
            detalle=payload['detalle'],
        ).exists()
        self.assertTrue(exists)

    def test_create_reporte_invalid(self):
        """Test creating invalid reporte fails"""
        payload = {'tipo': 2}
        res = self.client.post(REPORTES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
