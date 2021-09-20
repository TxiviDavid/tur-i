from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status,views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import PuntoInteres, Restaurante, Reporte
from core.models import GPXTrack, GPXPoint, TrackPoint

from recursos import serializers

from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Transform
from django.apps import apps
import requests,xmltodict, json


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
    queryset = PuntoInteres.objects.annotate(transformed=Transform("geom", 4326))
    serializer_class = serializers.PuntoInteresSerializer

    #def get_queryset(self):
        #"""Return objects for the current authenticated user only"""

        #return self.queryset.annotate(transformed=Transform("geom", 4326))
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'upload_image':
            return serializers.PuntoInteresImageSerializer
        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a poi"""
        poi = self.get_object()
        serializer = self.get_serializer(
            poi,
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


class RestauranteViewSet(BaseRecursosAttrViewSet):
    """Manage restaurnates in the database"""
    queryset = Restaurante.objects.annotate(transformed=Transform("geom", 4326))
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
        #"""Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """Create a new recurso"""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a new recurso"""
        request.data['signo'] = int(request.data['signo'])
        request.data['tipo'] = int(request.data['tipo'])
        request.data['detalle'] = int(request.data['detalle'])
        coord = request.data['geom'].split(sep=" ")
        request.data['geom'] = GEOSGeometry('POINT(' + coord[0] + ' ' + coord[1] + ')')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'upload_image':
            return serializers.ReporteImageSerializer
        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a reporte"""
        reporte = self.get_object()
        serializer = self.get_serializer(
            reporte,
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

class AlojamientoView(views.APIView):
    def get(self, request):
        response = requests.get('http://api.clubrural.com/api.php?claveapi=7ed46f8e1b54470882e5ef419a216203&type=provincias&idprov=31')
        #https://simpleisbetterthancomplex.com/tips/2016/11/01/django-tip-19-protecting-sensitive-information.html
        #https://simpleisbetterthancomplex.com/2015/11/26/package-of-the-week-python-decouple.html
        data = xmltodict.parse(response.text)
        dataarr = []
        alojamientos = data["api"]["alojamiento"]
        #alojamientos = [{"nombre": 10, "tipo": 0, "alquiler":"","animales":1,"piscina":1,"internet":1,"provincia":"","localidad":"","precio":33,"plazas":3,"url":"","lat":"","lng":""}, {"nombre": 10, "tipo": 0, "alquiler":"","animales":1,"piscina":1,"internet":1,"provincia":"","localidad":"","precio":33,"plazas":3,"url":"","lat":"","lng":""}]

        for al in alojamientos:
            dataarr.append(al)

        geojson = {
            "type": "FeatureCollection",
            "features": [
            {
                "type": "Feature",
                "geometry" : {
                    "type": "Point",
                    "coordinates": [d["lng"], d["lat"]],
                    },
                "properties" : d,
             } for d in dataarr]
}
        #data = [{"nombre": 10, "tipo": 0, "alquiler":"","animales":1,"piscina":1,"internet":1,"provincia":"","localidad":"","precio":33,"plazas":3,"url":"","lat":"","lng":""}, {"nombre": 10, "tipo": 0, "alquiler":"","animales":1,"piscina":1,"internet":1,"provincia":"","localidad":"","precio":33,"plazas":3,"url":"","lat":"","lng":""}]
        #data= [{"likes": 10, "comments": 0}, {"likes": 4, "comments": 23}]
        #results = serializers.AlojamientoSerializer(dataarr, many=True).data
        return Response(geojson)

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

class DominiosView(views.APIView):
    def get(self, request):
        dominios = []
        selected_modelPoi = apps.get_model('core', 'PuntoInteres')
        dominioTipo = selected_modelPoi.objects.values('tipo').distinct()
        selected_modelR = apps.get_model('core', 'Restaurante')
        dominioCocina = selected_modelR .objects.values('cocina').distinct()
        dominioPoblacion = selected_modelR .objects.values('poblacion').distinct()
        dominios.append({'tipo':dominioTipo})
        dominios.append({'cocina':dominioCocina})
        dominios.append({'poblacion':dominioPoblacion})
        return Response(dominios)
