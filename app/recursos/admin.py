# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from leaflet.admin import LeafletGeoAdmin
from core import models as recursos_models
from core.views import upload_gpx





class PuntoInteresImageInline(admin.TabularInline):
    model = recursos_models.PuntoInteresImage
    extra = 3


class PuntoInteresAdmin(LeafletGeoAdmin):
    list_display = ['nombre','tipo']
    list_filter = (
        ('tipo'),
        ('nombre')
    )
    list_per_page = 15
    inlines = [ PuntoInteresImageInline, ]

class ReportesAdmin(LeafletGeoAdmin):
    list_display = ['signo','tipo','detalle']
    list_filter = (
        ('signo'),
        ('tipo')
    )
    list_per_page = 15
    #inlines = [ PuntoInteresImageInline, ]

class RestauranteAdmin(LeafletGeoAdmin):
    list_display = ['cocina','nombre','poblacion']
    list_filter = (
        ('cocina'),
        ('poblacion')
    )
    list_per_page = 15

class StorymapAdmin(LeafletGeoAdmin):
    list_display = ['nombre','tipo']
    list_filter = (
        ('nombre'),
        ('tipo')
    )
    list_per_page = 15

class PlanAdmin(admin.ModelAdmin):
    list_display = ['nombre','user','shared']
    list_filter = (
        ('nombre'),
        ('user')
    )
    list_per_page = 15

class PlanMovilAdmin(admin.ModelAdmin):
    list_display = ['nombre','user','saved']
    list_filter = (
        ('nombre'),
        ('user')
    )
    list_per_page = 15

class RegionAdmin(LeafletGeoAdmin):
    list_display = ['nombre']
    list_filter = (
        ('nombre'),
    )
    list_per_page = 15

class EntradaAdmin(LeafletGeoAdmin):
    list_display = ['nombre']
    list_filter = (
        ('nombre'),
    )
    list_per_page = 15

class InteresAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    list_filter = (
        ('nombre'),
    )
    list_per_page = 15

class ModoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    list_filter = (
        ('nombre'),
    )
    list_per_page = 15

#esto es otro modo de anadir el modelo en el admin
@admin.register(recursos_models.GPXFile)
class FileAdmin(admin.ModelAdmin):
    #cuando queremos sobreescribir el metodo que salta al guardar el formulario en el admin
    def save_model(self, request, obj, form, change):
         # your login if you want to perform some comutation on save
         # it will help you if you need request into your work
         upload_gpx(request)


class GPXTrackAdmin(geoadmin.GeoModelAdmin):
    #map_template = 'leaflet/admin/widget.html'
    #GeoJSON = ''
    list_display = ['nombre','descripcion']
    #inlines = [
        #TrackPointsInline,
    #]

class GPXPointAdmin(LeafletGeoAdmin):
    list_display = ['nombre','descripcion']

class PruebaAdmin(LeafletGeoAdmin):
    map_template = 'leaflet/admin/widget.html'
    GeoJSON = ''


admin.site.register(recursos_models.PuntoInteres, PuntoInteresAdmin)
admin.site.register(recursos_models.Reporte, ReportesAdmin)

admin.site.register(recursos_models.GPXPoint, GPXPointAdmin)
admin.site.register(recursos_models.GPXTrack, GPXTrackAdmin)
admin.site.register(recursos_models.PruebaLine, PruebaAdmin)
admin.site.register(recursos_models.Restaurante, RestauranteAdmin)
admin.site.register(recursos_models.Storymap, StorymapAdmin)
admin.site.register(recursos_models.Plan, PlanAdmin)
admin.site.register(recursos_models.PlanMovil, PlanMovilAdmin)
admin.site.register(recursos_models.Region, RegionAdmin)
admin.site.register(recursos_models.Entrada, EntradaAdmin)
admin.site.register(recursos_models.Interes, InteresAdmin)
admin.site.register(recursos_models.Modo, ModoAdmin)