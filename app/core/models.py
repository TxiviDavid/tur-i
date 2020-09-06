
from django.db import models as models
from django.contrib.gis.db import models as geoModels
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings


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


class PuntoInteres(geoModels.Model):
    nombre = models.CharField("Nombre", max_length=50, blank=True)
    tipo = models.CharField(choices=Tipo.choices, max_length=50,
                            default=Tipo.BIODIVERSIDAD)
    descripcion = models.TextField("Descripción", max_length=1500, blank=True)
    observaciones = models.TextField("Observaciones", max_length=250,
                                     blank=True)
    geom = geoModels.PointField(srid=25830, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # objects = models.GeoManager()

    class Meta:
        verbose_name = 'Punto de Interés'
        verbose_name_plural = 'Puntos de Interés'

    # def __unicode__(self):
        # return unicode(self.nombre)

    def __str__(self):
        return self.nombre
