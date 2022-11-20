from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer,GeometrySerializerMethodField
from rest_framework_gis.fields import GeometryField
from django.contrib.gis.geos import Point

from core.models import PuntoInteres, Restaurante, Reporte, PuntoInteresImage, Plan, Storymap, PlanMovil, Region, Entrada, Interes
from core.models import GPXTrack, GPXPoint, TrackPoint




class PuntoInteresSerializer(GeoFeatureModelSerializer):
    """ A class to serialize PuntoInteres as GeoJSON compatible data """
    geom = GeometryField(source='transformed')
    #items = serializers.RelatedField(source='image',read_only=True)

    class Meta:
        model = PuntoInteres
        depth = 1 #para devolver la tabla relacional
        geo_field = "geom"
        fields = ('id', 'nombre','tipo','descripcion','observaciones','panorama360','tiempo','images','modelo3D','user','geom','region')
        read_only_Fields = ('id',)

class PuntoInteresImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to restaurante"""

    class Meta:
        model = PuntoInteres
        fields = ('id', 'image')
        read_only_fields = ('id',)

class RestauranteSerializer(GeoFeatureModelSerializer):
    """ A class to serialize Restaurante as GeoJSON compatible data """
    geom = GeometryField(source='transformed')

    class Meta:
        model = Restaurante
        geo_field = "geom"
        fields = ('id', 'nombre','cocina','direccion','poblacion','telefono','email','foto')
        read_only_Fields = ('id',)


class RestauranteImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to restaurante"""

    class Meta:
        model = Restaurante
        fields = ('id', 'foto')
        read_only_fields = ('id',)

class StorymapSerializer(GeoFeatureModelSerializer):
    """ A class to serialize Storymap as GeoJSON compatible data """
    geom = GeometryField(source='transformed')

    class Meta:
        model = Storymap
        geo_field = "geom"
        fields = ('id', 'nombre','tipo','descripcion','foto','user','geom')
        read_only_Fields = ('id',)


class StorymapImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to Storymap"""

    class Meta:
        model = Storymap
        fields = ('id', 'foto')
        read_only_fields = ('id',)

class ReporteSerializer(GeoFeatureModelSerializer):
    """ A class to serialize Reporte as GeoJSON compatible data """
    #geom = GeometryField(source='transformed')

    class Meta:
        model = Reporte
        geo_field = "geom"
        fields = ('id', 'signo', 'tipo', 'detalle','descripcion','foto')
        read_only_Fields = ('id',)


class ReporteImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to reporte"""

    class Meta:
        model = Reporte
        fields = ('id', 'foto')
        read_only_fields = ('id',)

class PlanSerializer(serializers.ModelSerializer):
    """ A class to serialize Plan Object"""

    class Meta:
        model = Plan
        fields = ('id', 'nombre', 'plan', 'foto', 'descripcion','shared')
        read_only_Fields = ('id',)

class PlanMovilSerializer(serializers.ModelSerializer):
    """ A class to serialize Plan Object"""

    class Meta:
        model = PlanMovil
        fields = ('id', 'plan')
        read_only_Fields = ('id',)

class RegionSerializer(serializers.ModelSerializer):
    """A class to serialize Region Object"""

    class Meta:
        model = Region
        fields = ('id', 'nombre', 'geom')
        read_only_fields = ('id',)

class EntradaSerializer(serializers.ModelSerializer):
    """A class to serialize Entrada Object"""

    class Meta:
        model = Entrada
        fields = ('id', 'nombre', 'region', 'geom')
        read_only_fields = ('id',)

class InteresSerializer(serializers.ModelSerializer):
    """A class to serialize Interes Object"""

    class Meta:
        model = Interes
        fields = ('id', 'nombre')
        read_only_fields = ('id',)
'''
https://stackoverflow.com/questions/45532965/django-rest-framework-serializer-without-a-model
class AlojamientoSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    tipo = serializers.CharField()
    alquiler = serializers.CharField()
    animales = serializers.CharField()
    piscina = serializers.CharField()
    internet = serializers.CharField()
    provincia = serializers.CharField()
    localidad = serializers.CharField()
    precio = serializers.CharField()
    plazas = serializers.CharField()
    url = serializers.CharField()
    lat = serializers.CharField()
    lng = serializers.CharField()
'''
class GPXTrackSerializer(GeoFeatureModelSerializer):
    """Serializer for GPXTrack object"""

    class Meta:
        model = GPXTrack
        geo_field = "geom"
        auto_bbox = True
        fields = ('id', 'nombre', 'tipo', 'matricula','dificultad','longitud','circular','foto','descripcion', 'gpx_fichero', 'geom')
        read_only_Fields = ('id',)


class GPXPointSerializer(serializers.ModelSerializer):
    """Serializer for GPXPoint object"""

    class Meta:
        model = GPXPoint
        fields = ('id', 'nombre', 'gpx_fichero', 'geom')
        read_only_Fields = ('id',)


class TrackPointSerializer(serializers.ModelSerializer):
    """Serializer for TrackPoint object"""

    class Meta:
        model = TrackPoint
        fields = ('id', 'nombre', 'sendero', 'descripcion', 'geom')
        read_only_Fields = ('id',)
