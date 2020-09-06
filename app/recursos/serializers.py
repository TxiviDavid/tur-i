from rest_framework import serializers

from core.models import PuntoInteres


class PuntoInteresSerializer(serializers.ModelSerializer):
    """Serializer for PuntoInteres object"""

    class Meta:
        model = PuntoInteres
        fields = ('id', 'nombre')
        read_only_Fields = ('id',)
