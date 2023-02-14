from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status,views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

from core.models import PuntoInteres, Restaurante, Reporte, Plan, Storymap, PlanMovil, Region, Entrada, Interes, Modo, Ruta, Provincia, Subregion
from core.models import GPXTrack, GPXPoint, TrackPoint

from recursos import serializers

from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Transform
from django.apps import apps
import requests,xmltodict, json
from rest_framework import status,serializers as sr
from rest_framework.exceptions import APIException
import os
from django.contrib.gis.utils import LayerMapping

class PlainValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid input."
    default_code = "invalid"

    def __init__(self, detail=None, code=None):
        if not isinstance(detail, dict):
            raise sr.ValidationError("Invalid Input")
        self.detail = detail

#class MyAuthentication(TokenAuthentication):
    #def authenticate_credentials(self, key):
        #try:
        #token = self.model.objects.select_related('user').get(key=key)
        #except self.model.DoesNotExist:
            # modify the original exception response
            #raise exceptions.AuthenticationFailed('Custom error message')
        #raise PlainValidationError({"status": 1,
                #"message": "token is not valid",})

        

        

class BaseRecursosAttrViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin):
    """Base viewset for user owned recursos attributes"""
    authentication_classes = (TokenAuthentication,) #TokenAuthentication
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-nombre')

    def perform_create(self, serializer):
        """Create a new recurso"""
        serializer.save(user=self.request.user)


class PuntoInteresViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
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


class RestauranteViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
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

class ReporteAllViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage puntosinteres in the database"""
    queryset = Reporte.objects.all()
    serializer_class = serializers.ReporteSerializer

    def get_queryset(self):
        #"""Return objects for the current authenticated user only"""
        return self.queryset.filter().order_by('-id')

class ReporteViewSet(BaseRecursosAttrViewSet):
    """Manage puntosinteres in the database"""
    queryset = Reporte.objects.all()
    serializer_class = serializers.ReporteSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
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

class StorymapViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage storympas in the database"""
    queryset = Storymap.objects.annotate(transformed=Transform("geom", 4326))
    serializer_class = serializers.StorymapSerializer

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'upload_image':
            return serializers.StorymapImageSerializer
        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a storymap"""
        storymap = self.get_object()
        serializer = self.get_serializer(
            storymap,
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

class PlanesSharedViewSet(BaseRecursosAttrViewSet):
    """Manage plan in the database"""
    queryset = Plan.objects.all()
    serializer_class = serializers.PlanSharedSerializer
    def get_queryset(self):
        #"""Return objects for the current id"""
        return self.queryset.filter(shared=True).order_by('-id')

class PlanSharedViewSet(BaseRecursosAttrViewSet):
    """Get shared plan by id"""
    queryset = Plan.objects.all()
    serializer_class = serializers.PlanSharedSerializer
    def get_queryset(self):
        #"""Return objects for the current id"""
        return self.queryset.filter(id=self.request.GET.get('id'), shared=True)

class PlanMovilViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage planMovil in the database"""
    queryset = PlanMovil.objects.all()
    serializer_class = serializers.PlanMovilSerializer
    def get_queryset(self):
        #"""Return objects for the current id"""
        return self.queryset.filter(id=self.request.GET.get('id'))

class PlansToMobilViewSet(BaseRecursosAttrViewSet):
    """Manage plan in the database"""
    queryset = Plan.objects.all()
    serializer_class = serializers.PlansForViewinMobilViewSetSerializer

    def get_queryset(self):
        #"""Return objects"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True, context={"request": request}) #metemos el contexto para que contruya el absolute path
        return Response({"planes":serializer.data})

class GetPlanException(APIException):
    status_code = 200
    default_detail = 'No existe el plan'
    default_code = 12


class PlanViewSet(BaseRecursosAttrViewSet):
    """Manage plan in the database"""
    queryset = Plan.objects.all()
    serializer_class = serializers.PlanSerializer

    def get_queryset(self):
        #"""Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """Create a new recurso"""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a new recurso"""
        request.data._mutable = True
        if 'plan' in request.data:
            request.data['plan'] = json.loads(request.data['plan'])
        request.data._mutable = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'upload_image':
            return serializers.PlanImageSerializer
        return self.serializer_class
    
    #def partial_update(self, request, *args, **kwargs):
        #shared = request.data['shared']
        #kwargs['partial'] = True
        #self.update(request, *args, **kwargs)
        #return Response({'shared':shared}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            instance = Plan.objects.get(id=pk)
            self.perform_destroy(instance)
            content = {'id': kwargs['pk']}
            return Response({'id':pk}, status=status.HTTP_200_OK)
        except:
            raise GetPlanException()

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a plan"""
        plan = self.get_object()
        serializer = self.get_serializer(
            plan,
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

class RutasViewSet(BaseRecursosAttrViewSet):
    """Manage planMovil in the database"""
    queryset = Ruta.objects.all()
    serializer_class = serializers.RutaSerializer
    def get_queryset(self):
        #"""Return objects for the current id"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

class RutaViewSet(BaseRecursosAttrViewSet):
    """Get shared plan by id"""
    queryset = Ruta.objects.all()
    serializer_class = serializers.RutaSerializer
    def get_queryset(self):
        #"""Return objects for the current id"""
        return self.queryset.filter(id=self.request.GET.get('id'), user=self.request.user)

class RutasSharedViewSet(BaseRecursosAttrViewSet):
    """Manage plan in the database"""
    queryset = Ruta.objects.all()
    serializer_class = serializers.RutaSerializer
    def get_queryset(self):
        #"""Return objects for the current id"""
        return self.queryset.filter(shared=True).order_by('-id')

class RutaSharedViewSet(BaseRecursosAttrViewSet):
    """Get shared plan by id"""
    queryset = Ruta.objects.all()
    serializer_class = serializers.RutaSerializer
    def get_queryset(self):
        #"""Return objects for the current id"""
        return self.queryset.filter(id=self.request.GET.get('id'), shared=True)

#https://docs.djangoproject.com/en/4.1/ref/contrib/gis/layermapping/#layermapping-api
class RegionesGeoJSONViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage regiones as geojson in the database"""
    queryset = Region.objects.annotate(transformed=Transform("geom", 4326))
    serializer_class = serializers.RegionGeoJSONSerializer

class SubregionesGeoJSONViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage regiones as geojson in the database"""
    queryset = Subregion.objects.annotate(transformed=Transform("geom", 4326))
    serializer_class = serializers.SubregionGeoJSONSerializer


class RegionMovilView(views.APIView):
    """Manage region in the database"""

    def get(self, request, **kwargs):
        my_data = Subregion.objects.all()
        serializer = self.get_serializer('first',my_data)
        return Response({"regiones":serializer.data})


    def get_serializer(self,type,data):
        my_serializers = {
        'first':serializers.SubregionMovilSerializer(data,many=True),
        }
        return my_serializers[type]

class SubregionView(views.APIView):
    """Manage region in the database"""

    def get(self, request, **kwargs):
        my_data = Subregion.objects.all()
        serializer = self.get_serializer('first',my_data)
        return Response({"subregiones":serializer.data})
 

    def get_serializer(self,type,data):
        my_serializers = {
        'first':serializers.SubregionSerializer(data,many=True),
        }
        return my_serializers[type]

class ProvinciaView(views.APIView):
    """Manage provincia in the database"""

    def get(self, request, **kwargs):
        my_data = Provincia.objects.all()
        serializer = self.get_serializer('first',my_data)
        return Response({"provincias":serializer.data})


    def get_serializer(self,type,data):
        my_serializers = {
        'first':serializers.ProvinciaSerializer(data,many=True),
        }
        return my_serializers[type]

#https://stackoverflow.com/questions/48506898/what-are-the-differences-between-generics-views-viewsets-and-mixins-in-django

class EntradaViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage entrada in the database"""
    queryset = Entrada.objects.all()
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset.filter(region=self.request.GET.get('regionId'))

    def list(self, request):
        serializer = serializers.EntradaSerializer(self.get_queryset(), many=True)
        return Response({"entradas":serializer.data})

class InteresViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage interes in the database"""
    queryset = Interes.objects.all()
    serializer_class = serializers.InteresSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"intereses":serializer.data})

class ModoViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage modo in the database"""
    queryset = Modo.objects.all()
    serializer_class = serializers.InteresSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"modos":serializer.data})

class AlojamientoView(views.APIView):
    def get(self, request):
        response = requests.get('http://api.clubrural.com/api.php?claveapi=7ed46f8e1b54470882e5ef419a216203&type=provincias&idprov=31')
        #https://simpleisbetterthancomplex.com/tips/2016/11/01/django-tip-19-protecting-sensitive-information.html
        #https://simpleisbetterthancomplex.com/2015/11/26/package-of-the-week-python-decouple.html
        data = xmltodict.parse(response.text)
        dataarr = []
        alojamientos = data["api"]["alojamiento"]
        #alojamientos = [{"nombre": 10, "tipo": 0, "alquiler":"","animales":1,"piscina":1,"internet":1,"provincia":"","localidad":"","precio":33,"plazas":3,"url":"","lat":"","lng":""}, {"nombre": 10, "tipo": 0, "alquiler":"","animales":1,"piscina":1,"internet":1,"provincia":"","localidad":"","precio":33,"plazas":3,"url":"","lat":"","lng":""}]

        for idx,al in enumerate(alojamientos):
            al['idAlojamiento'] = idx + 1
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

class GPXTrackViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
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

class InsertRegionsView(views.APIView):
    def get(self, request):
        region_mapping = {
            'nombre' : 'SUBZONA',
            'geom' : 'POLYGON',
        }

        data_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../regions/subregions.shp'))
        print(data_shp)
        lm = LayerMapping(Subregion, data_shp, region_mapping,
                      transform=False, encoding='iso-8859-1')
        lm.save(strict=True, verbose=True)
        return Response()
