from rest_framework import serializers

from core.models import PuntoInteres, Restaurante, Reporte
from core.models import GPXTrack, GPXPoint, TrackPoint


class PuntoInteresSerializer(serializers.ModelSerializer):
    """Serializer for PuntoInteres object"""

    class Meta:
        model = PuntoInteres
        fields = ('id', 'nombre')
        read_only_Fields = ('id',)


class RestauranteSerializer(serializers.ModelSerializer):
    """Serializer for Restaurante object"""

    class Meta:
        model = Restaurante
        fields = ('id', 'nombre')
        read_only_Fields = ('id',)


class RestauranteImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to restaurante"""

    class Meta:
        model = Restaurante
        fields = ('id', 'foto')
        read_only_fields = ('id',)


class ReporteSerializer(serializers.ModelSerializer):
    """Serializer for Reporte object"""

    class Meta:
        model = Reporte
        fields = ('id', 'signo', 'tipo', 'detalle')
        read_only_Fields = ('id',)


class GPXTrackSerializer(serializers.ModelSerializer):
    """Serializer for GPXTrack object"""

    class Meta:
        model = GPXTrack
        fields = ('id', 'nombre', 'tipo', 'matricula', 'gpx_fichero', 'geom')
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
