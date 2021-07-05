from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import PuntoInteres, Restaurante, Reporte
from core.models import GPXTrack, GPXPoint, TrackPoint

from recursos import serializers


class BaseRecursosAttrViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Base viewset for user owned recursos attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-nombre')

    def perform_create(self, serializer):
        """Create a new recurso"""
        serializer.save(user=self.request.user)


class PuntoInteresViewSet(BaseRecursosAttrViewSet):
    """Manage puntosinteres in the database"""
    queryset = PuntoInteres.objects.all()
    serializer_class = serializers.PuntoInteresSerializer


class RestauranteViewSet(BaseRecursosAttrViewSet):
    """Manage puntosinteres in the database"""
    queryset = Restaurante.objects.all()
    serializer_class = serializers.RestauranteSerializer

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'upload_image':
            return serializers.RestauranteImageSerializer
        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a restaurante"""
        restaurante = self.get_object()
        serializer = self.get_serializer(
            restaurante,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ReporteViewSet(BaseRecursosAttrViewSet):
    """Manage puntosinteres in the database"""
    queryset = Reporte.objects.all()
    serializer_class = serializers.ReporteSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-id')


class GPXTrackViewSet(BaseRecursosAttrViewSet):
    """Manage puntosinteres in the database"""
    queryset = GPXTrack.objects.all()
    serializer_class = serializers.GPXTrackSerializer


class GPXPointViewSet(BaseRecursosAttrViewSet):
    """Manage puntosinteres in the database"""
    queryset = GPXPoint.objects.all()
    serializer_class = serializers.GPXPointSerializer


class TrackPointViewSet(BaseRecursosAttrViewSet):
    """Manage puntosinteres in the database"""
    queryset = TrackPoint.objects.all()
    serializer_class = serializers.TrackPointSerializer
