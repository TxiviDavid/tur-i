from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recursos import views


router = DefaultRouter()
router.register('puntosInteres', views.PuntoInteresViewSet)
router.register('restaurantes', views.RestauranteViewSet)
router.register('reportes', views.ReporteAllViewSet)
router.register('reportesSigno', views.SignoReportesDominiosViewSet)
router.register('reportesTipoPositivo', views.TipoReportesPositivoDominiosViewSet)
router.register('reportesTipoNegativo', views.TipoReportesNegativoDominiosViewSet)
router.register('reportesTipo', views.TipoReportesDominiosViewSet)
router.register('reportesDetalle', views.DetalleReportesDominiosViewSet)
router.register('reportesDetalleVista', views.DetalleVistaReportesDominiosViewSet)
router.register('reportesDetalleInteresante', views.DetalleInteresanteReportesDominiosViewSet)
router.register('reportesDetalleBienvenida', views.DetalleBienvenidaReportesDominiosViewSet)
router.register('reportesDetalleFauna', views.DetalleFaunaReportesDominiosViewSet)
router.register('reportesDetalleFlora', views.DetalleFloraReportesDominiosViewSet)
router.register('reportesDetallePuente', views.DetallePuenteReportesDominiosViewSet)
router.register('reportesDetalleIntimidatorio', views.DetalleIntimidatorioReportesDominiosViewSet)
router.register('reportesDetalleObstruccion', views.DetalleObstruccionReportesDominiosViewSet)
router.register('reportesDetalleSuperficie', views.DetalleSuperficieReportesDominiosViewSet)
router.register('reportesDetalleCruce', views.DetalleCruceReportesDominiosViewSet)
router.register('reportesDetalleIndicacion', views.DetalleIndicacionReportesDominiosViewSet)
router.register('reportesEdit', views.ReporteViewSet)
router.register('storymaps', views.StorymapViewSet)
router.register('rutaShared', views.RutaSharedViewSet)
router.register('rutasShared', views.RutasSharedViewSet)
router.register('rutas', views.RutasViewSet)
router.register('ruta', views.RutaViewSet)
router.register('planes', views.PlanViewSet)
router.register('planesMovil', views.PlanMovilViewSet)
router.register('plansToMovil', views.PlansToMobilViewSet)
router.register('planesShared', views.PlanesSharedViewSet)
router.register('planShared', views.PlanSharedViewSet)
router.register('entradas', views.EntradaViewSet)
router.register('regionesGeoJSON', views.RegionesGeoJSONViewSet)
router.register('subregionesGeoJSON', views.SubregionesGeoJSONViewSet)
router.register('intereses', views.InteresViewSet)
router.register('modos', views.ModoViewSet)
router.register('GPXTrack', views.GPXTrackViewSet)
router.register('GPXPoint', views.GPXPointViewSet)
router.register('TrackPoint', views.TrackPointViewSet)

app_name = 'recursos'

urlpatterns = [
    path('', include(router.urls))
]
