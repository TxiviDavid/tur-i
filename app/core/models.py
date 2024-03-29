
import uuid
import os
from django.db import models as models
from django.contrib.gis.db import models as geoModels
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings
from django.utils.timezone import now


def regiones_image_file_path(instance, filename):
    """Generate file path for new regiones image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/regiones/', filename)

def subregiones_image_file_path(instance, filename):
    """Generate file path for new subregiones image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/subregiones/', filename)


def punto_interes_image_file_path(instance, filename):
    """Generate file path for new puntoInteres image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/puntointeres/', filename)


def restaurante_image_file_path(instance, filename):
    """Generate file path for new restaurante image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/restaurante/', filename)


def reporte_image_file_path(instance, filename):
    """Generate file path for new reporte image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/reporte/', filename)

def storymap_image_file_path(instance, filename):
    """Generate file path for new storymap image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/storymap/', filename)

def plan_image_file_path(instance, filename):
    """Generate file path for new plan image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/plan/', filename)


def gpxtrack_image_file_path(instance, filename):
    """Generate file path for new gpxtrack image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/gpxtrack/', filename)


class Usermanager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = Usermanager()

    USERNAME_FIELD = 'email'


class Tipo(models.TextChoices):
    BIODIVERSIDAD = 'BIODIVERSIDAD', 'Biodiversidad'
    ARQUEOLOGICO = 'ARQUEOLOGICO', 'Historia y arqueología'
    ARQUITECTURA = 'ARQUITECTURA', 'Arquitectura'
    AGUA = 'AGUA', 'Zonas de agua'
    OTROS = 'OTROS', 'Otros'
    AREA_RECREATIVA = 'AREA_RECREATIVA', 'Área recreativa'
    PUNTO_ESPECIAL_INTERES = 'PUNTO_ESPECIAL_INTERES', 'Especial interés'
    MIRADOR = 'MIRADOR', 'Mirador'
    GEOLOGIA = 'GEOLOGIA', 'Geologia'

class StorymapsType(models.TextChoices):
    HISTORIA = 'HISTORIA', 'Historia'
    MITOLOGIA = 'MITOLOGIA', 'Mitologia'
    FOLCLORE = 'FOLCLORE', 'Folclore'
    MUSICA = 'MUSICA', 'Musica'
    DEPORTE = 'DEPORTE', 'Deporte'

class SignoReporte(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'SignoReporte'
        verbose_name_plural = 'SignosReporte'

    def __str__(self):
        return str(self.nombre)

class TipoReporte(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'TipoReporte'
        verbose_name_plural = 'TiposReporte'

    def __str__(self):
        return str(self.nombre)

class DetalleReporte(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'DetalleReporte'
        verbose_name_plural = 'DetallesReporte'

    def __str__(self):
        return str(self.nombre)

class Provincia(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'

    def __str__(self):
        return str(self.nombre)

class Region(geoModels.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    geom = geoModels.MultiPolygonField(srid=4326, blank=True, null=True)
    descripcion = models.TextField("Descripción", max_length=1500, blank=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.ForeignKey(Provincia,on_delete=models.CASCADE, null=True, related_name='regiones')

    class Meta:
        verbose_name = 'Región'
        verbose_name_plural = 'Regiones'

    def __str__(self):
        return str(self.nombre)

class RegionImage(models.Model):
    region = models.ForeignKey(Region, related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to=regiones_image_file_path, blank=True, null=True)

    class Meta:
        verbose_name = 'Material multimedia de las subregiones'
        verbose_name_plural = 'Materiales multimedia de las subregiones'

class Subregion(geoModels.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    geom = geoModels.MultiPolygonField(srid=4326, blank=True, null=True)
    descripcion = models.TextField("Descripción", max_length=1500, blank=True)
    enabled = models.BooleanField(null=False, default=False)
    region = models.ForeignKey(Region,on_delete=models.CASCADE, null=True, related_name='subregiones')

    class Meta:
        verbose_name = 'Subregión'
        verbose_name_plural = 'Subregiones'

    def __str__(self):
        return str(self.nombre)

class SubregionImage(models.Model):
    subregion = models.ForeignKey(Subregion, related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to=subregiones_image_file_path, blank=True, null=True)

    class Meta:
        verbose_name = 'Material multimedia de las subregiones'
        verbose_name_plural = 'Materiales multimedia de las subregiones'

class Entrada(geoModels.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    region = models.ManyToManyField(Region)
    geom = geoModels.PointField(srid=4326, blank=True, null=True)

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self):
        return str(self.nombre)

class Modo(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Modo'
        verbose_name_plural = 'Modos'

    def __str__(self):
        return str(self.nombre)

class Interes(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Interés'
        verbose_name_plural = 'Intereses'

    def __str__(self):
        return str(self.nombre)

class PuntoInteres(geoModels.Model):
    nombre = models.CharField("Nombre", max_length=50, null=False, blank=False)
    tipo = models.CharField(choices=Tipo.choices, max_length=50,
                            default=Tipo.BIODIVERSIDAD)
    descripcion = models.TextField("Descripción", max_length=1500, blank=True)
    observaciones = models.TextField("Observaciones", max_length=250,
                                     blank=True)
    panorama360 = models.ImageField(upload_to='panoramas/',
                                    blank=True, null=True)
    #foto = models.ImageField(upload_to=punto_interes_image_file_path,
                             #blank=True, null=True)
    tiempo = models.DecimalField(max_digits=4, decimal_places=1, default=1,
                                 blank=True)
    modelo3D = models.CharField(max_length=254, blank=True)
    geom = geoModels.PointField(srid=25830, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    subregion = models.ForeignKey(Subregion,on_delete=models.CASCADE)
    # objects = models.GeoManager()

    class Meta:
        verbose_name = 'Punto de Interés'
        verbose_name_plural = 'Puntos de Interés'

    # def __unicode__(self):
        # return unicode(self.nombre)

    def __str__(self):
        return str(self.nombre)

class PuntoInteresImage(models.Model):
    puntoInteres = models.ForeignKey(PuntoInteres, related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to=punto_interes_image_file_path, blank=True, null=True)

    class Meta:
        verbose_name = 'Material multimedia de los puntos de interés'
        verbose_name_plural = 'Materiales multimedia de los puntos de interés'


class Cocina(models.TextChoices):
    CASERA = 'CASERA', 'Casera'
    ASIATICO = 'ASIATICO', 'Asiático'
    SIDRERIA = 'SIDRERIA', 'Sidreria'
    PIZZERIA = 'PIZZERIA', 'Pizzeria'
    ASADOR = 'ASADOR', 'Asador'


class Restaurante(geoModels.Model):
    cocina = models.CharField(choices=Cocina.choices, max_length=50,
                              default=Cocina.CASERA)
    nombre = models.CharField("Nombre", max_length=50, null=False, blank=False)
    direccion = models.CharField(max_length=254, null=True)
    poblacion = models.CharField(max_length=254, null=True)
    telefono = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=254, blank=True, null=True)
    foto = models.ImageField(upload_to=restaurante_image_file_path,
                             blank=True, null=True)
    geom = geoModels.PointField(srid=25830, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'

    def __str__(self):
        return str(self.nombre)


class Reporte(geoModels.Model):
    signo = models.IntegerField(null=False)
    tipo = models.IntegerField(null=False)
    detalle = models.IntegerField(null=False)
    foto = models.ImageField(upload_to=reporte_image_file_path,
                             blank=True, null=True)
    descripcion = models.CharField(max_length=254, blank=True, null=True)
    geom = geoModels.PointField(srid=4326, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'

    def __int__(self):
        return self.id

class Storymap(geoModels.Model):
    nombre = models.CharField("Nombre", max_length=50, null=False, blank=False)
    tipo = models.CharField(choices=StorymapsType.choices, max_length=50,
                            default=StorymapsType.HISTORIA)
    foto = models.ImageField(upload_to=storymap_image_file_path,
                             blank=True, null=True)
    descripcion = models.CharField(max_length=254, blank=True, null=True)
    geom = geoModels.PointField(srid=4326, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Storymap'
        verbose_name_plural = 'Storymaps'

    def __int__(self):
        return self.nombre

class Plan(geoModels.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    plan = models.JSONField()
    foto = models.ImageField(upload_to=plan_image_file_path,
                             blank=True, null=True)
    descripcion = models.CharField(max_length=254, blank=True, null=True)
    gpx = models.JSONField(blank=True, null=True)
    shared = models.BooleanField(null=False, default=False)
    creationDate = models.DateTimeField(default=now, blank=False)
    modificationDate = models.DateTimeField(default=now, blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'

    def __int__(self):
        return self.nombre

class PlanMovil(geoModels.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    plan = models.JSONField()
    foto = models.ImageField(upload_to=plan_image_file_path,
                             blank=True, null=True)
    descripcion = models.CharField(max_length=254, blank=True, null=True)
    shared = models.BooleanField(null=False, default=False)
    saved = models.BooleanField(null=False, default=False)
    savedPlan = models.IntegerField(null=True, default=False)
    creationDate = models.DateTimeField(default=now, blank=False)
    modificationDate = models.DateTimeField(default=now, blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'PlanMovil'
        verbose_name_plural = 'PlanesMovil'

    def __int__(self):
        return self.nombre

class Signo(models.Model):
    signo = models.IntegerField(null=True)
    significado = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.significado)


class Tipo(models.Model):
    tipo = models.IntegerField(null=True)
    significado = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.significado)


class Detalle(models.Model):
    detalle = models.IntegerField(null=True)
    significado = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.significado)

class Ruta(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    puntos = models.JSONField()
    path = models.JSONField()
    gpx = models.JSONField(blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    shared = models.BooleanField(null=False, default=False)
    creationDate = models.DateTimeField(default=now, blank=False)
    modificationDate = models.DateTimeField(default=now, blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True
    )

class TrackType(models.TextChoices):
    SENDEROS_HOMOLOGADOS = 'SENDEROS_HOMOLOGADOS', 'Senderos homologados'
    RED_CAMINOS = 'RED_CAMINOS', 'Red de caminos'
    CAMINOS_NATURALES = 'CAMINOS_NATURALES', 'Caminos naturales'
    OTROS = 'OTROS', 'Otros'

def GPX_Folder(instance, filename):
    return "uploaded_gpx_files/%s" % (filename)


class GPXFile(models.Model):
    nombre = models.CharField("Nombre", max_length=100)
    gpx_fichero = models.FileField(upload_to=GPX_Folder)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Fichero GPX'
        verbose_name_plural = 'Ficheros GPX'

    def __str__(self):
        return str(self.nombre)


class Matricula(models.TextChoices):
    SL = 'SL', 'SL'
    PR = 'PR', 'PR'
    GR = 'GR', 'GR'


class Circular(models.TextChoices):
    SI = 'SI', 'Si'
    NO = 'NO', 'No'


class Dificultad(models.TextChoices):
    FACIL = 'FACIL', 'Fácil'
    MODERADO = 'MODERADO', 'Moderado'
    DIFICIL = 'DIFICIL', 'Difícil'


class GPXTrack(geoModels.Model):
    nombre = models.CharField("Nombre", max_length=50, blank=True)
    tipo = models.CharField(choices=TrackType.choices, max_length=50,
                            default=TrackType.SENDEROS_HOMOLOGADOS)
    matricula = models.CharField(choices=Matricula.choices, max_length=50,
                                 default=Matricula.PR)
    circular = models.CharField(choices=Circular.choices, max_length=2,
                                default=Circular.SI)
    longitud = models.FloatField(null=True, blank=True)
    dificultad = models.CharField(choices=Dificultad.choices, max_length=20,
                                  default=Dificultad.FACIL)
    descripcion = models.TextField("Descripción", max_length=250,
                                   blank=True)
    observaciones = models.TextField("Observaciones", max_length=250,
                                     blank=True)
    foto = models.ImageField(upload_to=gpxtrack_image_file_path,
                             blank=True, null=True)
    geom = geoModels.MultiLineStringField(dim=3)
    gpx_fichero = models.ForeignKey(GPXFile, null=False,
                                    on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # objects = models.GeoManager()

    class Meta:
        verbose_name = 'Sendero GPX'
        verbose_name_plural = 'Senderos GPX'

    def __str__(self):
        return str(self.nombre)


class GPXPoint(geoModels.Model):
    nombre = models.CharField("Nombre", max_length=50, blank=True)
    descripcion = models.CharField("Descripción", max_length=250, blank=True)
    gpx_fichero = models.ForeignKey(GPXFile, null=False,
                                    on_delete=models.CASCADE)
    geom = geoModels.PointField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # objects = models.GeoManager()

    class Meta:
        verbose_name = 'Punto GPX'
        verbose_name_plural = 'Puntos GPX'

    def __str__(self):
        return str(self.nombre)


class TrackPoint(geoModels.Model):
    nombre = models.CharField("Nombre", max_length=50, blank=True)
    descripcion = models.CharField("Descripción", max_length=250, blank=True)
    sendero = models.ForeignKey('GPXTrack', null=False,
                                on_delete=models.CASCADE)
    geom = geoModels.PointField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # objects = models.GeoManager()

    class Meta:
        verbose_name = 'Punto GPX'
        verbose_name_plural = 'Puntos GPX'

    def __str__(self):
        return str(self.nombre)

class PruebaLine(geoModels.Model):
    nombre = models.CharField("Nombre", max_length=50, blank=True)
    descripcion = models.CharField("Descripción", max_length=250, blank=True)
    geom = geoModels.MultiLineStringField(dim=3)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # objects = models.GeoManager()


    def __str__(self):
        return str(self.nombre)
