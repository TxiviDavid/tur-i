from rest_framework import serializers

from core.models import PuntoInteres, Restaurante


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
