from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer,GeometrySerializerMethodField
from rest_framework_gis.fields import GeometryField
from django.contrib.gis.geos import Point

from core.models import PuntoInteres, Restaurante, Reporte, PuntoInteresImage, Plan, Storymap, PlanMovil, Region, Entrada, Interes, Modo, Ruta, Subregion, Provincia
from core.models import GPXTrack, GPXPoint, TrackPoint


class PuntoInteresImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to restaurante"""

    class Meta:
        model = PuntoInteresImage
        fields = ('id', 'image','puntoInteres')
        read_only_fields = ('id',)

class PuntoInteresSerializer(GeoFeatureModelSerializer):
    """ A class to serialize PuntoInteres as GeoJSON compatible data """
    geom = GeometryField(source='transformed')
    #images = serializers.CharField(source='image.image', required=True) 
    #items = serializers.RelatedField(source='image',read_only=True)
    images = PuntoInteresImageSerializer(many=True)
    idPoi = serializers.IntegerField(source='id')

    class Meta:
        model = PuntoInteres
        #depth = 1 #para devolver la tabla relacional
        geo_field = "geom"
        fields = ('id','idPoi', 'nombre','tipo','descripcion','observaciones','panorama360','tiempo','images','modelo3D','user','geom','subregion')
        read_only_Fields = ('id',)



class RestauranteSerializer(GeoFeatureModelSerializer):
    """ A class to serialize Restaurante as GeoJSON compatible data """
    geom = GeometryField(source='transformed')
    idRestaurante = serializers.IntegerField(source='id')

    class Meta:
        model = Restaurante
        geo_field = "geom"
        fields = ('id', 'idRestaurante', 'nombre','cocina','direccion','poblacion','telefono','email','foto')
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

class PlanSharedSerializer(serializers.ModelSerializer):
    """ A class to serialize Plan Object"""
    userName = serializers.CharField(source='user.name', required=False)   
    class Meta:
        model = Plan
        fields = ('id', 'nombre', 'plan', 'foto', 'descripcion','shared','creationDate','modificationDate','userName')
        read_only_Fields = ('id',)

class PlanSerializer(serializers.ModelSerializer):
    """ A class to serialize Plan Object"""
    userName = serializers.CharField(source='user.name', required=False)   
    class Meta:
        model = Plan
        fields = ('id', 'nombre', 'plan', 'foto', 'descripcion', 'gpx', 'shared','creationDate','modificationDate','userName')
        read_only_Fields = ('id',)

class PlanMovilSerializer(serializers.ModelSerializer):
    """ A class to serialize Plan Object"""

    class Meta:
        model = PlanMovil
        fields = ('id', 'plan')
        read_only_Fields = ('id',)

class PlansForViewinMobilViewSetSerializer(serializers.ModelSerializer):
    """ A class to serialize Plan Object"""
    #https://stackoverflow.com/questions/35522768/django-serializer-imagefield-to-get-full-url
    userName = serializers.CharField(source='user.name', required=False)
    #photo_url = serializers.SerializerMethodField()
    foto = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = Plan
        fields = ('id', 'nombre', 'foto', 'descripcion','shared','creationDate','userName')
        read_only_Fields = ('id',)

    def get_photo_url(self, plan):
        request = self.context.get('request')
        try:
            photo_url = plan.foto.url
        except:
            photo_url = None
        return request.build_absolute_uri(photo_url)

class RutaSerializer(serializers.ModelSerializer):
    """ A class to serialize Plan Object"""
    userName = serializers.CharField(source='user.name', required=False)   
    class Meta:
        model = Ruta
        fields = ('id', 'nombre', 'puntos', 'path', 'gpx', 'tipo', 'shared','creationDate','modificationDate','userName')
        read_only_Fields = ('id',)

class RegionGeoJSONSerializer(GeoFeatureModelSerializer):
    """A class to serialize Region Object as geojson"""
    geom = GeometryField(source='transformed')
    provinciaName = serializers.CharField(source='provincia.nombre', required=False)
    provinciaId = serializers.IntegerField(source='provincia.id', required=False)
    #items = serializers.RelatedField(source='image',read_only=True)

    class Meta:
        model = Region
        geo_field = "geom"
        fields = ('id', 'nombre', 'geom','provinciaName','provinciaId')
        read_only_Fields = ('id',)

class SubregionGeoJSONSerializer(GeoFeatureModelSerializer):
    """A class to serialize Region Object as geojson"""
    geom = GeometryField(source='transformed')
    regionName = serializers.CharField(source='region.nombre', required=False)
    regionId = serializers.IntegerField(source='region.id', required=False)
    regionColor = serializers.CharField(source='region.color', required=False)

    class Meta:
        model = Subregion
        geo_field = "geom"
        depth = 1
        fields = ('id', 'nombre','enabled','descripcion','images', 'geom','regionName','regionId','regionColor')
        read_only_Fields = ('id',)

class SubregionMovilSerializer(serializers.ModelSerializer):
    """A class to serialize Region Object"""   
    class Meta:
        model = Subregion
        fields = ('id', 'nombre')
        read_only_fields = ('id',)

class SubregionSerializer(serializers.ModelSerializer):
    """A class to serialize Subregion Object"""
    #regionName = serializers.CharField(source='region.nombre', required=False)
    #regionId = serializers.IntegerField(source='region.id', required=False)
    #provinciaName = serializers.CharField(source='region.provincia.nombre', required=False)
    #provinciaId = serializers.IntegerField(source='region.provincia.id', required=False)

    class Meta:
        model = Subregion
        fields = ('id', 'nombre','enabled')
        read_only_fields = ('id',)

class RegionSerializer(serializers.ModelSerializer):
    """A class to serialize Region Object"""
    subregiones = SubregionSerializer( many=True)
    
    class Meta:
        model = Region
        fields = ('id', 'nombre','subregiones')
        read_only_fields = ('id',)

class ProvinciaSerializer(serializers.ModelSerializer):
    """A class to serialize Provincia Object"""
    #regiones = serializers.SlugRelatedField(
        #many=True,
        #read_only=True,
        #slug_field='nombre'
    #)
    #subregiones =serializers.SerializerMethodField()
    regiones = RegionSerializer( many=True)


    class Meta:
        model = Provincia
        fields = ('id', 'nombre','regiones')
        read_only_fields = ('id',)

    #def get_subregiones(self,obj):
        #cat = Subregion.objects.get(id=1)
        #print(cat)
        #return cat.nombre

class EntradaSerializer(serializers.ModelSerializer):
    """A class to serialize Entrada Object"""

    class Meta:
        model = Entrada
        fields = ('id', 'nombre', 'geom')
        read_only_fields = ('id',)

class InteresSerializer(serializers.ModelSerializer):
    """A class to serialize Interes Object"""

    class Meta:
        model = Interes
        fields = ('id', 'nombre')
        read_only_fields = ('id',)

class ModoSerializer(serializers.ModelSerializer):
    """A class to serialize Modo Object"""

    class Meta:
        model = Modo
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
    idRuta = serializers.IntegerField(source='id')

    class Meta:
        model = GPXTrack
        geo_field = "geom"
        auto_bbox = True
        fields = ('id','idRuta', 'nombre', 'tipo', 'matricula','dificultad','longitud','circular','foto','descripcion', 'gpx_fichero', 'geom')
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
