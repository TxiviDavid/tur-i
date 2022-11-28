from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recursos import views


router = DefaultRouter()
router.register('puntosInteres', views.PuntoInteresViewSet)
router.register('restaurantes', views.RestauranteViewSet)
router.register('reportes', views.ReporteViewSet)
router.register('storymaps', views.StorymapViewSet)
router.register('planes', views.PlanViewSet)
router.register('planesMovil', views.PlanMovilViewSet)
router.register('entradas', views.EntradaViewSet)
router.register('regionesGeoJSON', views.RegionesGeoJSONViewSet)
router.register('intereses', views.InteresViewSet)
router.register('modos', views.ModoViewSet)
router.register('GPXTrack', views.GPXTrackViewSet)
router.register('GPXPoint', views.GPXPointViewSet)
router.register('TrackPoint', views.TrackPointViewSet)

app_name = 'recursos'

urlpatterns = [
    path('', include(router.urls))
]
