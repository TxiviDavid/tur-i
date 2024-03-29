from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status,views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

from core.models import PuntoInteres, Restaurante, Reporte, Plan, Storymap, PlanMovil, Region, Entrada, Interes, Modo, Ruta, Provincia, Subregion, SignoReporte, TipoReporte, DetalleReporte
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
#import overpy
import requests

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
        request.data._mutable = True
        request.data['signo'] = int(request.data['signo'])
        request.data['tipo'] = int(request.data['tipo'])
        request.data['detalle'] = int(request.data['detalle'])
        coord = request.data['geom'].split(sep=" ")
        request.data['geom'] = GEOSGeometry('POINT(' + coord[0] + ' ' + coord[1] + ')')
        request.data._mutable = False
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
        #return self.queryset.filter(region=self.request.GET.get('regionId'))
        return self.queryset.filter()

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

class DominiosMovilView(views.APIView):
    def get(self, request):
        dominiosPois = []
        dominiosRestaurantes = []
        dominiosRutas = []
        dominiosReportes = []
        dominiosMultimedia = []
        dominiosRutasTipo = [{'nombre':'FACIL'},{'nombre':'DIFICIL'},{'nombre':'CORTA'},{'nombre':'LARGA'},{'nombre':'CIRCULAR'},{'nombre':'HOMOLOGADA'}]
        dominiosMultimediaTipo = [{'nombre':'MODELO3D'},{'nombre':'PANORAMA360'}]
        dominiosReportesTipo = [{'nombre':'POSITIVO'},{'nombre':'NEGATIVO'}]
        selected_modelPoi = apps.get_model('core', 'PuntoInteres')
        dominioTipo = list(selected_modelPoi.objects.values('tipo').distinct())
        for d in dominioTipo:
            d['nombre'] = d.pop('tipo').upper().replace('_',' ')    
        selected_modelR = apps.get_model('core', 'Restaurante')
        dominioCocina = list(selected_modelR .objects.values('cocina').distinct())
        for d in dominioCocina:
            d['nombre'] = d.pop('cocina').upper() 
        dominioPoblacion = list(selected_modelR .objects.values('poblacion').distinct())
        for d in dominioPoblacion:
            d['nombre'] = d.pop('poblacion').upper() 
        dominiosPois.append({'tipo':list(dominioTipo)})
        dominiosRestaurantes.append({'tipo':dominioCocina})
        dominiosRestaurantes.append({'poblacion':dominioPoblacion})
        dominiosRutas.append({'tipo':dominiosRutasTipo})
        dominiosReportes.append({'tipo':dominiosReportesTipo})
        dominiosMultimedia.append({'tipo':dominiosMultimediaTipo})
        return Response({"restaurantes":dominiosRestaurantes,"rutas":dominiosRutas,"pois":dominiosPois,"reportes":dominiosReportes,"multimedia":dominiosMultimedia})

class SignoReportesDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage SignoReporte in the database"""
    queryset = SignoReporte.objects.all()
    serializer_class = serializers.SignoReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"signo":serializer.data})

class TipoReportesDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage TipoReporte in the database"""
    queryset = TipoReporte.objects.all()
    serializer_class = serializers.TipoReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"tipo":serializer.data})

class TipoReportesPositivoDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage TipoReporte in the database"""
    queryset = TipoReporte.objects.filter(id__gt=0, id__lt=6)
    serializer_class = serializers.TipoReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"tipo":serializer.data})

class TipoReportesNegativoDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage TipoReporte in the database"""
    queryset = TipoReporte.objects.filter(id__gt=5, id__lt=13)
    serializer_class = serializers.TipoReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"tipo":serializer.data})

class DetalleReportesDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage DetalleReporte in the database"""
    queryset = DetalleReporte.objects.all()
    serializer_class = serializers.DetalleReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"detalle":serializer.data})

        
class DetalleVistaReportesDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage DetalleVistaReportes in the database"""
    queryset = DetalleReporte.objects.filter(id__gt=0, id__lt=7)
    serializer_class = serializers.DetalleReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"detalle":serializer.data})

class DetalleInteresanteReportesDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage DetalleInteresanteReportes in the database"""
    queryset = DetalleReporte.objects.filter(id__gt=6, id__lt=14)
    serializer_class = serializers.DetalleReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"detalle":serializer.data})
        
class DetalleBienvenidaReportesDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage DetalleBienvenidaReportes in the database"""
    queryset = DetalleReporte.objects.filter(id__gt=13, id__lt=17)
    serializer_class = serializers.DetalleReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"detalle":serializer.data})

class DetalleFaunaReportesDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage DetalleFaunaReportes in the database"""
    queryset = DetalleReporte.objects.filter(id__gt=16, id__lt=23)
    serializer_class = serializers.DetalleReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"detalle":serializer.data})

class DetalleFloraReportesDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage DetalleFloraReportes in the database"""
    queryset = DetalleReporte.objects.filter(id__gt=22, id__lt=27)
    serializer_class = serializers.DetalleReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"detalle":serializer.data})

class DetallePuenteReportesDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage DetallePuenteReportes in the database"""
    queryset = DetalleReporte.objects.filter(id__gt=26, id__lt=33)
    serializer_class = serializers.DetalleReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"detalle":serializer.data})

class DetalleIntimidatorioReportesDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage DetalleIntimidatorioReportes in the database"""
    queryset = DetalleReporte.objects.filter(id__gt=32, id__lt=39)
    serializer_class = serializers.DetalleReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"detalle":serializer.data})

class DetalleObstruccionReportesDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage DetalleObstruccionReportes in the database"""
    queryset = DetalleReporte.objects.filter(id__gt=38, id__lt=46)
    serializer_class = serializers.DetalleReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"detalle":serializer.data})

class DetalleSuperficieReportesDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage DetalleSuperficieReportes in the database"""
    queryset = DetalleReporte.objects.filter(id__gt=45, id__lt=51)
    serializer_class = serializers.DetalleReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"detalle":serializer.data})

class DetalleCruceReportesDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage DetalleCruceReportes in the database"""
    queryset = DetalleReporte.objects.filter(id__gt=50, id__lt=53)
    serializer_class = serializers.DetalleReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"detalle":serializer.data})

class DetalleIndicacionReportesDominiosViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Manage DetalleIndicacionReportes in the database"""
    queryset = DetalleReporte.objects.filter(id__gt=52, id__lt=58)
    serializer_class = serializers.DetalleReporteSerializer
    def get_queryset(self):
        #"""Return objects"""
        return self.queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response({"detalle":serializer.data})

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

class LoadPoisView(views.APIView):
    def get(self, request):
        #https://www.openstreetmap.org/query?lat=42.81940&lon=-1.64123#map=15/42.8194/-1.6412
        #https://wiki.openstreetmap.org/wiki/Map_features
        #api = overpy.Overpass()
        api=None

        query_result = api.query("""
            area["wikidata" = "Q4018"]->.place;    
            node["amenity"="place_of_worship"](area.place);
                (._;>;);
                out body;
            """)


        #points_array = [ GEOSGeometry('POINT(' + str(x.lon) + ' ' + str(x.lat) + ')') for x in query_result.nodes]
        #points_series = gpd.GeoSeries(points_array)

        monuments_array = [ { 
            "name": x.tags.get("name", ""),
            "name:en": x.tags.get("name:en", ""),
            "geom": str(GEOSGeometry('POINT(' + str(x.lon) + ' ' + str(x.lat) + ')'))
        } for x in query_result.nodes]

        #monuments_gdf = gpd.GeoDataFrame(monuments_array, geometry=points_series, crs=4326)
        return Response(monuments_array)

class LoadImagesView(views.APIView):
    def get_request_url(self,**kwargs):
        url='https://www.googleapis.com/customsearch/v1?'
        param=''.join(['{}={}&'.format(k,kwargs[k]) for k in kwargs])
        url += param
        return url

    def search_images_google(self, query='example'):
        # https://developers.google.com/custom-search/v1/reference/rest/v1/ImgType?hl=es-419
        params = {
            'key':'AIzaSyCs3RPvnmmZ3QCyab56JuuA6BK4WPAEqvY',
            'cx':'a7e6477e537566d39',
            'q': query,
            'searchType': 'image',
            'imgSize': 'large',
            'imgColorType':'color',
            'imgType':'photo',
            'num':10,
            'start':1,
            'filter':1
        }
        urls = []
        for n_query in range(params['num']):
            url = self.get_request_url(**params)
            response = requests.get(url)
            response.raise_for_status()
            results = response.json()
            len_page = len(results['items'])
            for item in range(len_page):
                urls.append(results['items'][item]['link'])
            params['start'] += params['num']
        return list(urls)

    def get(self, request):
        ims = self.search_images_google('Alsasua pueblo')

        

        #monuments_gdf = gpd.GeoDataFrame(monuments_array, geometry=points_series, crs=4326)
        return Response(ims)
