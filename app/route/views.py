from django.shortcuts import render
from rest_framework import viewsets, mixins, status,views
import json
from rest_framework.response import Response
import openrouteservice
from django.core.serializers.json import DjangoJSONEncoder

class RouteView(views.APIView):
    def get(self, request):
        return Response(request)

    def post(self, request):

        client = openrouteservice.Client(key='5b3ce3597851110001cf62487a683d8abb1243bda57c5455b3c8985e')
        request_params = request.data
        route_normal = client.directions(**request_params)


        context = {
            'data':route_normal,
        }
        return Response(context, status=status.HTTP_200_OK)
