"""turi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from recursos import views
from plan.views import PlanView
from planMovil.views import PlanMovilView, MovePoiPlanView, DeletePoiPlanView, CommentPoiPlanView, ReviewPoiPlanView, SavePlanView, EditPlanView, GetPlanMovil, SharePlan
from route.views import RouteView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/recursos/', include('recursos.urls')),
    path('api/recursos/alojamientos/', views.AlojamientoView.as_view()),
    path('api/recursos/dominios/', views.DominiosView.as_view()),
    path('api/recursos/insertregions/', views.InsertRegionsView.as_view()),
    path('api/recursos/loadpois/', views.LoadPoisView.as_view()),
    path('api/recursos/loadimages/', views.LoadImagesView.as_view()),
    path('api/recursos/provincias/', views.ProvinciaView.as_view()),
    path('api/recursos/regiones/', views.RegionMovilView.as_view()),
    path('api/recursos/subregiones/', views.SubregionView.as_view()),
    path('api/plan/', PlanView.as_view()),
    path('api/planMovil/', PlanMovilView.as_view()),
    path('api/movePoiPlanMovil/', MovePoiPlanView.as_view()),
    path('api/deletePoiPlanMovil/', DeletePoiPlanView.as_view()),
    path('api/commentPoiPlanMovil/', CommentPoiPlanView.as_view()),
    path('api/reviewPoiPlanMovil/', ReviewPoiPlanView.as_view()),
    path('api/savePlanMovil/', SavePlanView.as_view()),
    path('api/editPlanMovil/', EditPlanView.as_view()),
    path('api/getPlanMovil/', GetPlanMovil.as_view()),
    path('api/sharePlan/', SharePlan.as_view()),
    path('api/route/', RouteView.as_view()),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    )
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,)
