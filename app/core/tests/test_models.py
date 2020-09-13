import mock
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point, LineString, MultiLineString
from django.core.files import File

from core import models


def sample_user(email='test@londonappdev.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """Test creating a new user with email is sucessful"""
        email = 'test@londonappdev.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user"""
        email = 'test@LONDONAPPDEV.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            # anything here should raise the ValueError
            get_user_model().objects.create_user(None, 'test123')

    def test_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@londonappdev.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_PuntoInteres_str(self):
        """Test the puntoInteres string representation"""
        PuntoInteres = models.PuntoInteres.objects.create(
            user=sample_user(),
            nombre='Monasterio'
        )

        self.assertEqual(str(PuntoInteres), PuntoInteres.nombre)

    def test_Restaurante_str(self):
        """Test the restaurante string representation"""
        Restaurante = models.Restaurante.objects.create(
            user=sample_user(),
            nombre='Piko'
        )

        self.assertEqual(str(Restaurante), Restaurante.nombre)

    def test_Reporte_str(self):
        """Test the reporte id representation"""
        Reporte = models.Reporte.objects.create(
            user=sample_user(),
            signo=2,
            tipo=2,
            detalle=2,
        )

        self.assertEqual(int(Reporte), Reporte.id)

    def test_GPXTrack_str(self):
        """Test the GPXTrack representation"""
        GPXFile = models.GPXFile.objects.create(
            user=sample_user(email='test@londonappdevuu.com',
                             password='testpassuu'),
            nombre="Arakil",
        )
        ls1 = LineString((0, 0, 0), (1, 1, 1))
        ls2 = LineString((2, 2, 2), (3, 3, 3))
        mls = MultiLineString(ls1, ls2)
        GPXTrack = models.GPXTrack.objects.create(
            user=sample_user(),
            nombre="ArakArakñól",
            tipo="Otros",
            gpx_fichero=GPXFile,
            geom=mls
        )

        self.assertEqual(str(GPXTrack), GPXTrack.nombre)

    def test_GPXFile_str(self):
        """Test the GPXFile representation"""
        file_mock = mock.MagicMock(spec=File, name='FileMock')
        file_mock.name = 'test1.jpg'
        GPXFile = models.GPXFile.objects.create(
            user=sample_user(),
            nombre="Arakil",
            gpx_fichero=file_mock
        )

        self.assertEqual(str(GPXFile), GPXFile.nombre)

    def test_GPXPoint_str(self):
        """Test the GPXPoint representation"""
        GPXFile = models.GPXFile.objects.create(
            user=sample_user(email='test@londonappdevuu.com',
                             password='testpassuu'),
            nombre="Arakil",
        )
        GPXPoint = models.GPXPoint.objects.create(
            user=sample_user(),
            nombre="Arakil",
            gpx_fichero=GPXFile,
            geom=Point(5, 23)
        )

        self.assertEqual(str(GPXPoint), GPXPoint.nombre)

    def test_TrackPoint_str(self):
        """Test the TrackPoint representation"""
        GPXFile = models.GPXFile.objects.create(
            user=sample_user(email='test@londonappdevuu.com',
                             password='testpassuu'),
            nombre="Arakil",
        )
        ls1 = LineString((0, 0, 0), (1, 1, 1))
        ls2 = LineString((2, 2, 2), (3, 3, 3))
        mls = MultiLineString(ls1, ls2)
        GPXTrack = models.GPXTrack.objects.create(
            user=sample_user(email='test@londonapfda.com',
                             password='testpfdasuu'),
            nombre="ArakArakñól",
            tipo="Otros",
            gpx_fichero=GPXFile,
            geom=mls
        )

        TrackPoint = models.TrackPoint.objects.create(
            user=sample_user(),
            nombre="Arakil",
            sendero=GPXTrack,
            geom=Point(5, 23)
        )

        self.assertEqual(str(TrackPoint), TrackPoint.nombre)

    @patch('uuid.uuid4')
    def test_punto_interes_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.punto_interes_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/puntointeres/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)

    @patch('uuid.uuid4')
    def test_restaurante_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.restaurante_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/restaurante/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)

    @patch('uuid.uuid4')
    def test_reporte_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.reporte_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/reporte/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)

    @patch('uuid.uuid4')
    def test_gpxtrack_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.gpxtrack_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/gpxtrack/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
