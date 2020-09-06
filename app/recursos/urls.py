from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recursos import views


router = DefaultRouter()
router.register('puntosInteres', views.PuntoInteresViewSet)

app_name = 'recursos'

urlpatterns = [
    path('', include(router.urls))
]
