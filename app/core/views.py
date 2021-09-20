# -*- coding: utf-8 -*-
from __future__ import unicode_literals


#from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.gis.gdal import SpatialReference, CoordTransform
#from django.utils.datetime_safe import datetime
from django.views import View
from django.contrib.gis.db.models.functions import Distance
#from osgeo import gdal,ogr
#from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Polygon
#from django.contrib.gis.measure import D


import json
from geojson import Feature as FeatureGeoJSON, Point as PointGeoJSOn, FeatureCollection


from django.http import HttpResponse

from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.gis.geos import Point, LineString, MultiLineString

from core.forms import UploadGpxForm
from core.models import GPXPoint, GPXTrack, GPXFile

from django.conf import settings

import gpxpy
import gpxpy.gpx
import random
from django.core.serializers import serialize






# function for parsing and saving data from gpx file to our database
# function is called after the gpx_file is uploaded
def SaveGPXtoPostGIS(f, file_instance,request):
    gpx_file = open(settings.MEDIA_ROOT + '/uploaded_gpx_files' + '/' + f.name)
    gpx = gpxpy.parse(gpx_file)

    if gpx.waypoints:
        for waypoint in gpx.waypoints:
            new_waypoint = GPXPoint()
            if waypoint.name:
                new_waypoint.nombre = waypoint.name
            else:
                new_waypoint.nombre = 'unknown'
            new_waypoint.geom = Point(waypoint.longitude, waypoint.latitude)
            new_waypoint.gpx_fichero = file_instance
            new_waypoint.user = request.user
            new_waypoint.save()

    if gpx.tracks:
        for track in gpx.tracks:
            print ("track name:" + str(track.name))
            new_track = GPXTrack()
            for segment in track.segments:
                track_list_of_points = []
                for point in segment.points:
                    point_in_segment = Point(point.longitude, point.latitude,point.elevation)
                    track_list_of_points.append(point_in_segment.coords)

                new_track_segment = LineString(track_list_of_points)
            new_track.nombre = file_instance
            new_track.geom = MultiLineString(new_track_segment)
            new_track.gpx_fichero = file_instance
            new_track.user = request.user
            new_track.save()


def upload_gpx(request):
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        file_instance = GPXFile()
        form = UploadGpxForm(request.POST, request.FILES, instance=file_instance)
        args['form'] = form
        if form.is_valid():
            form.save()
            SaveGPXtoPostGIS(request.FILES['gpx_fichero'], file_instance,request)

            return HttpResponse(status=204)

    else:
        args['form'] = UploadGpxForm()

    return render(request,'myapp/form.html', args)


def upload_success(request):
    return render(request,'myapp/success.html')
