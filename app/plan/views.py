from django.shortcuts import render
from rest_framework import viewsets, mixins, status,views
import requests,xmltodict, json
from rest_framework.response import Response
from django.db.models import Q
from core.models import PuntoInteres,PuntoInteresImage
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.gdal import SpatialReference, CoordTransform
import openrouteservice
import json
import math
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from dateutil.relativedelta import relativedelta
from django.utils.datetime_safe import datetime,date,strftime,new_date
from django.utils.dateformat import format
# Create your views here.

class PlanView(views.APIView):
    def get(self, request):
        return Response(request)

    def post(self, request):

        #estacion = request.data['estacion']
        Entrada = request.data['entrada']
        Gusto = request.data['interes']
        modo = request.data['modo']
        fechaLlegada = request.data['fechaLlegada']
        fechaSalida = request.data['fechaSalida']
        Llegada = request.data['timepickerLlegada']
        Llegada=int(Llegada)
        Salida= request.data['timepickerSalida']
        Salida=int(Salida)
        Inicial= request.data['timepickerInicio']
        Inicial=Inicial.split(':')
        Inicial=int(Inicial[0])
        Final = request.data['timepickerFin']
        Final=Final.split(':')
        Final=int(Final[0])

        #vamos a hacer un select por distancia con los filtros de atributos
        # creamos un objeto Q vacio
        q_object = Q()
        try:
            biodiversidad = Gusto.index('1')
            q_object.add(Q(**{'tipo__contains': 'BIODIVERSIDAD'}), Q.OR)
        except:
            existe = 'no existe'
        try:
            biodiversidad = Gusto.index('2')
            q_object.add(Q(**{'tipo__contains': 'GEOLOGIA'}), Q.OR)
        except:
            existe = 'no existe'
        try:
            biodiversidad = Gusto.index('3')
            q_object.add(Q(**{'tipo__contains': 'ARQUEOLOGICO'}), Q.OR)
        except:
            existe = 'no existe'
        try:
            biodiversidad = Gusto.index('4')
            q_object.add(Q(**{'tipo__contains': 'ARQUITECTURA'}), Q.OR)
        except:
            existe = 'no existe'
        try:
            biodiversidad = Gusto.index('5')
            q_object.add(Q(**{'tipo__contains': 'AGUA'}), Q.OR)
        except:
            existe = 'no existe'
        try:
            biodiversidad = Gusto.index('6')
            q_object.add(Q(**{'tipo__contains': 'AREA_RECREATIVA'}), Q.OR)
        except:
            existe = 'no existe'
        try:
            biodiversidad = Gusto.index('7')
            q_object.add(Q(**{'tipo__contains': 'PUNTO_ESPECIAL_INTERES'}), Q.OR)
        except:
            existe = 'no existe'
        try:
            biodiversidad = Gusto.index('8')
            q_object.add(Q(**{'tipo__contains': 'MIRADOR'}), Q.OR)
        except:
            existe = 'no existe'
        try:
            biodiversidad = Gusto.index('9')
            q_object.add(Q(**{'tipo__contains': 'PRODUCTOS'}), Q.OR)
        except:
            existe = 'no existe'
        try:
            biodiversidad = Gusto.index('10')
            q_object.add(Q(**{'tipo__contains': 'ACTIVIDADES'}), Q.OR)
        except:
            existe = 'no existe'
        try:
            biodiversidad = Gusto.index('11')
            q_object.add(Q(**{'tipo__contains': 'OTROS'}), Q.OR)
        except:
            existe = 'no existe'

        # obtenemos el resultado de los filtros
        Filtros = PuntoInteres.objects.filter(q_object)
        if Entrada == '1':
            latitude = '42.904467'
            longitud = '-1.822357'
        elif Entrada ==  '2':
            latitude = '42.935674'
            longitud = '-1.828988'
        elif Entrada == '3':
            latitude = '42.865774'
            longitud = '-2.240841'
        elif Entrada == '4':
            latitude = '42.932579'
            longitud = '-2.228765'
        puntoInicio = GEOSGeometry('POINT(' + longitud + ' ' + latitude + ')')
        gcoord = SpatialReference(4326)
        mycoord = SpatialReference(25830)
        trans = CoordTransform(gcoord, mycoord)
        puntoInicio.transform(trans)
        recursoInicio = PuntoInteres.objects.filter(q_object).annotate(
            distance=Distance('geom', puntoInicio)).order_by('distance')


        imagenesRecursos = []
        for punto in recursoInicio:
            imagenesPunto = PuntoInteresImage.objects.filter(puntoInteres=punto)
            imagenes = []
            contador = 0
            for imagenPunto in imagenesPunto:
                #if contador==0:
                    foto = str(imagenPunto.image.name)
                    imagenes.append(foto)
                    contador +=1

            imagenesRecursos.append(imagenes)



        #convertimos a lista para posteriormente poder borrar elementos de las listas
        imagenesRecursos = list(imagenesRecursos)
        tiempos = list(recursoInicio.values('tiempo'))
        nombreRecursos = list(recursoInicio.values('nombre'))
        descipcionRecursos = list(recursoInicio.values('descripcion'))
        geometriaRecursos = list(recursoInicio.values('geom'))
        tipoRecursos = list(recursoInicio.values('tipo'))
        observacionesRecursos = list(recursoInicio.values('observaciones'))
        fotosRecursos = list(recursoInicio.values('images'))

        # ORS
        #recursos_dict = {}
        recursosNombres_arr = []
        recursosNombres_arr.append({'nombre':'Comienzo'})
        for nombre in nombreRecursos:
            recursosNombres_arr.append(nombre)
        recursos_arr = []
        recursos_arr.append([float(longitud), float(latitude)])
        h = 1
        client = openrouteservice.Client(key='5b3ce3597851110001cf62487a683d8abb1243bda57c5455b3c8985e')
        for geometriaRecurso in geometriaRecursos:
            h += 2
            punto = GEOSGeometry(
                'POINT(' + str(geometriaRecurso['geom'].x) + ' ' + str(geometriaRecurso['geom'].y) + ')')
            gcoord = SpatialReference(25830)
            mycoord = SpatialReference(4326)
            trans = CoordTransform(gcoord, mycoord)
            punto.transform(trans)
            x = punto.x
            y = punto.y
            #recursos_dict['' + str(h) + ''] = {'location': [x, y]}
            recursos_arr.append([x, y])
        radiuses = [2000] * len(recursos_arr)
        request_params = {'coordinates': recursos_arr,
                          'radiuses': radiuses,
                          'format_out': 'geojson',
                          'profile': 'driving-car',
                          'preference': 'shortest',

                          'instructions': 'true', }
        route_normal = client.directions(**request_params)
        dataJson = route_normal['features'][0]['geometry']
        geojson = json.dumps(dataJson, cls=DjangoJSONEncoder)
        duracion_total_horas = 20
        #duracion_total_horas = route_normal['features'][0]['properties']['summary']['duration'] / 3600.00
        # Round a number to the closest half integer.
        duracion_total_horas_rounded = 0.5 * math.ceil(2.0 * duracion_total_horas)
        duracionSegmentos = list()
        segmentos =  route_normal['features'][0]['properties']['segments']
        for segmento in segmentos:
            duracion = round(segmento['duration']/3600,2)
            duracionSegmentos.append(duracion)
        duracionIndex = 0


        #PLANNING
        fechaLlegada = fechaLlegada.split('-')
        fechaSalida =  fechaSalida.split('-')
        diaLlegada = int(fechaLlegada[2])
        mesLlegada = int(fechaLlegada[1])
        anoLlegada = int(fechaLlegada[0])
        diaSalida = int(fechaSalida[2])
        mesSalida = int(fechaSalida[1])
        anoSalida = int(fechaSalida[0])


        fechaLlegada = datetime(anoLlegada, mesLlegada, diaLlegada,Llegada)
        fechaSalida = datetime(anoSalida, mesSalida, diaSalida,Salida)
        fechaLlegadaSinHora = date(anoLlegada, mesLlegada, diaLlegada)
        fechaSalidaSinHora = date(anoSalida, mesSalida, diaSalida)
        fechaSiguienteSinHora = date(anoLlegada, mesLlegada, diaLlegada)
        numeroDias = fechaSalidaSinHora - fechaLlegadaSinHora
        numeroDias = numeroDias.days +1
        diff = fechaSalida - fechaLlegada
        dias = diff.days
        horasDiarias = Final - Inicial

        horasUtiles = 0
        recursoIndex = 1
        imagenesPlan = imagenesRecursos
        tiemposPlan = tiempos
        nombreRecursosPlan = nombreRecursos
        descipcionRecursosPlan = descipcionRecursos
        diasPlan = dias
        plan = []

        html = ''
        #html += '<div role="tabpanel" class="tab-pane active" id="homePlan">'
        html += '<div id="mainPanelItinerario">'
        html += '<div id="diaPorDia">'
        if dias >= 0:
            if horasDiarias > 0:
                # preparamos el html de la tabla de los resultados
                html += '<div>'
                horasPrimerDia = 0
                if Final < Llegada:
                    horasPrimerDia = 0
                else:
                    mismoDia = fechaLlegada + relativedelta(hour=Final)
                    horasPrimerDia = Final - Llegada
                    comprobarUltimoDia = fechaSalidaSinHora - fechaLlegadaSinHora
                    if comprobarUltimoDia.days <= 0:
                        horasPrimerDia = diff.seconds
                        horasPrimerDia = horasPrimerDia / 3600
                        print('inicio: '+ str(fechaLlegada))
                        for i in range(horasPrimerDia):
                            horasUtiles+=1
                            print(fechaLlegada + relativedelta(hours=+(i + 1)))
                        print('Horas dia 1:' +str(horasPrimerDia))
                        html += '<div class="dayBlock">'
                        html += '<div class="dia-container">'
                        html += '<p class="font-weight-bold dark-grey-text">'+str(fechaLlegadaSinHora)+'</p><hr class="my-5">'
                        html += '</div>'
                        acumulacionTiempo = 0
                        recursos = 0
                        try:
                            acumulacionTiempo = acumulacionTiempo + Decimal(duracionSegmentos[duracionIndex])
                        except:
                            acumulacionTiempo = 0
                        itemsPlan = []
                        for index,tiempo in enumerate(tiempos):
                            tiempoRecurso = tiempo.get('tiempo')
                            if acumulacionTiempo <= horasPrimerDia:
                                recursos+=1
                                nombreRecurso = nombreRecursos[index].get('nombre')
                                descipcionRecurso = descipcionRecursos[index].get('descripcion')
                                tipoRecurso = tipoRecursos[index].get('tipo')
                                observacionesRecurso = observacionesRecursos[index].get('observaciones')
                                fotosRecurso = fotosRecursos[index].get('images')
                                html += '<div class="itinerarioRuta">'
                                html += '<div class="left-col-ruta"></div>'
                                html += '<div class="right-col-ruta">'
                                duracion = '0'
                                try:
                                    duracion = str(int(duracionSegmentos[duracionIndex] * 60))
                                    html += '<span class="travel-time"><i class="fa fa-car" aria-hidden="true"></i>  ' + str(
                                        int(duracionSegmentos[duracionIndex] * 60)) + ' minutos</span>'
                                except:
                                    html += ''
                                html += '</div>'
                                html += '</div>'
                                html += '<div class="itinerario">'
                                html += '<div class="contenidoVisita">'
                                html += '<div class="left-col">'
                                hora=fechaLlegada + relativedelta(hours=+float(acumulacionTiempo))
                                horaConDesplazamiento = hora + relativedelta(minutes=+int(duracionSegmentos[duracionIndex]))

                                duracionIndex+=1
                                try:
                                    acumulacionTiempo = tiempoRecurso + acumulacionTiempo + Decimal(duracionSegmentos[duracionIndex])
                                except:
                                    acumulacionTiempo = 0
                                html += '<p class="font-weight-bold dark-grey-text"><mdb-icon far icon="clock" class="pr-2"</mdb-icon> ' + str(horaConDesplazamiento.time()) + '</p>'
                                html += '</div>'
                                html += '<div class="row">'
                                html += '<div class="col-lg-5">'
                                html += '<div class="view overlay rounded z-depth-2 mb-lg-0 mb-4 waves-light" mdbWavesEffect><img class="img-fluid" src="https://mdbootstrap.com/img/Photos/Others/img (28).jpg"/></div>'
                                html += '</div>'
                                html += '<div class="col-lg-7">'
                                html += '<a href="#!" class="indigo-text"><h6 class="font-weight-bold mb-3"><mdb-icon fas icon="suitcase" class="pr-2"></mdb-icon>Travels</h6></a>'
                                html += '<h3 class="font-weight-bold mb-3"><strong>' + nombreRecurso + '</strong></h3>'
                                html += '<p>' + descipcionRecurso + '</p>'
                                html += '<p><strong>Tiempo de visita estimado:</strong> ' + str(tiempoRecurso) + ' h</p>'
                                html += '<button type="button" mdbBtn color="primary" mdbWavesEffect>Primary</button>'
                                html += '</div>'
                                html += '</div>'
                                html += '</div>'
                                html += '</div>'
                                html += '<div class="line-between"></div>'
                                itemsPlan.append([str(recursoIndex),duracion,str(horaConDesplazamiento.time()),nombreRecurso,descipcionRecurso,str(tiempoRecurso),tipoRecurso,observacionesRecurso,imagenesRecursos[index]])
                                recursoIndex = recursoIndex + 1
                        html += '</div>'
                        plan.append({str(fechaLlegadaSinHora):itemsPlan})
                        #eliminamos los recursos que ya hemos usado
                        del imagenesRecursos[0:recursos]
                        del tiempos[0:recursos]
                        del nombreRecursos[0:recursos]
                        del descipcionRecursos[0:recursos]
                        del tipoRecursos[0:recursos]
                        del observacionesRecursos[0:recursos]
                        del fotosRecursos[0:recursos]
                        print('fin')

                    else:
                        print('inicio: '+str(fechaLlegada))
                        for i in range(horasPrimerDia):
                            horasUtiles +=1
                            print(fechaLlegada + relativedelta(hours=+(i+1)))
                        print('Horas dia 1:'+ str(horasPrimerDia))
                        html += '<div class="dayBlock">'
                        html += '<div class="dia-container">'
                        html += '<p class="font-weight-bold dark-grey-text">'+str(fechaLlegadaSinHora)+'</p><hr class="my-5">'
                        html += '<div class="line-between"></div>'
                        html += '</div>'
                        acumulacionTiempo = 0
                        recursos = 0
                        try:
                            acumulacionTiempo = acumulacionTiempo + Decimal(duracionSegmentos[duracionIndex])
                        except:
                            acumulacionTiempo = 0
                        itemsPlan = []
                        for index, tiempo in enumerate(tiempos):
                            tiempoRecurso = tiempo.get('tiempo')
                            if acumulacionTiempo <= horasPrimerDia:
                                recursos += 1
                                nombreRecurso = nombreRecursos[index].get('nombre')
                                descipcionRecurso = descipcionRecursos[index].get('descripcion')
                                tipoRecurso = tipoRecursos[index].get('tipo')
                                observacionesRecurso = observacionesRecursos[index].get('observaciones')
                                fotosRecurso = fotosRecursos[index].get('images')
                                html += '<div class="itinerarioRuta">'
                                html += '<div class="left-col-ruta"></div>'
                                html += '<div class="right-col-ruta">'
                                duracion = '0'
                                try:
                                    duracion = str(int(duracionSegmentos[duracionIndex] * 60))
                                    html += '<hr class="my-5"><span class="travel-time"><i class="fa fa-car" aria-hidden="true"></i>  ' + str(
                                        int(duracionSegmentos[duracionIndex] * 60)) + ' minutos</span>'
                                except:
                                    html += ''
                                html += '</div>'
                                html += '</div>'
                                html += '<div class="itinerario">'
                                html += '<div class="contenidoVisita">'
                                html += '<div class="left-col">'
                                hora = fechaLlegada + relativedelta(hours=+float(acumulacionTiempo))
                                horaConDesplazamiento = hora + relativedelta(
                                    minutes=+int(duracionSegmentos[duracionIndex]))

                                duracionIndex+=1
                                try:
                                    acumulacionTiempo = tiempoRecurso + acumulacionTiempo + Decimal(
                                        duracionSegmentos[duracionIndex])
                                except:
                                    acumulacionTiempo = 0
                                html += '<p class="font-weight-bold dark-grey-text"><mdb-icon far icon="clock" class="pr-2"</mdb-icon> ' + str(horaConDesplazamiento.time()) + '</p>'
                                html += '</div>'
                                html += '<div class="row">'
                                html += '<div class="col-lg-5">'
                                html += '<div class="view overlay rounded z-depth-2 mb-lg-0 mb-4 waves-light" mdbWavesEffect><img class="img-fluid" src="https://mdbootstrap.com/img/Photos/Others/img (28).jpg"/></div>'
                                html += '</div>'
                                html += '<div class="col-lg-7">'
                                html += '<a href="#!" class="indigo-text"><h6 class="font-weight-bold mb-3"><mdb-icon fas icon="suitcase" class="pr-2"></mdb-icon>Travels</h6></a>'
                                html += '<h3 class="font-weight-bold mb-3"><strong>' + nombreRecurso + '</strong></h3>'
                                html += '<p>' + descipcionRecurso + '</p>'
                                html += '<p><strong>Tiempo de visita estimado:</strong> ' + str(tiempoRecurso) + ' h</p>'
                                html += '<button type="button" mdbBtn color="primary" mdbWavesEffect>Primary</button>'
                                html += '</div>'
                                html += '</div>'
                                html += '</div>'
                                html += '</div>'
                                html += '<div class="line-between"></div>'
                                itemsPlan.append([str(recursoIndex),duracion,str(horaConDesplazamiento.time()),nombreRecurso,descipcionRecurso,str(tiempoRecurso),tipoRecurso,observacionesRecurso,imagenesRecursos[index]])
                                recursoIndex = recursoIndex + 1
                        html += '</div>'
                        plan.append({str(fechaLlegadaSinHora):itemsPlan})
                        # eliminamos los recursos que ya hemos usado
                        del imagenesRecursos[0:recursos]
                        del tiempos[0:recursos]
                        del nombreRecursos[0:recursos]
                        del descipcionRecursos[0:recursos]
                        del tipoRecursos[0:recursos]
                        del observacionesRecursos[0:recursos]
                        del fotosRecursos[0:recursos]

                #segundo dia
                if numeroDias > 1:
                    fechaSiguienteSinHora = fechaSiguienteSinHora+ relativedelta(days=+1)
                    nuevoDiaInicio = fechaLlegada + relativedelta(days=+1, hour=Inicial)
                    nuevoDiaFin = nuevoDiaInicio + relativedelta(hour=Final)
                    #comprobamos si la fecha coincide con el ultimo dia
                    comprobarUltimoDia= fechaSalidaSinHora - fechaSiguienteSinHora
                    if comprobarUltimoDia.days <= 0:
                        horasDiarias = fechaSalida - nuevoDiaInicio
                        horasDiarias = horasDiarias.seconds
                        horasDiarias = horasDiarias//3600
                        print('inicio: '+ str(nuevoDiaInicio))
                        for i in range(horasDiarias):
                            horasUtiles +=1
                            print(nuevoDiaInicio + relativedelta(hours=+(i+1)))
                        print('Horas dia 2:' + str(horasDiarias))
                        print('fin')
                        html += '<div class="dayBlock">'
                        html += '<div class="dia-container">'

                        html += '<p class="font-weight-bold dark-grey-text">'+str(fechaSiguienteSinHora)+'</p><hr class="my-5">'
                        html += '</div>'
                        html += '<div class="line-between"></div>'
                        acumulacionTiempo = 0
                        recursos = 0
                        try:
                            acumulacionTiempo = acumulacionTiempo + Decimal(duracionSegmentos[duracionIndex])
                        except:
                            acumulacionTiempo = 0
                        itemsPlan = []
                        for index, tiempo in enumerate(tiempos):
                            tiempoRecurso = tiempo.get('tiempo')
                            if acumulacionTiempo <= horasDiarias:
                                recursos += 1
                                nombreRecurso = nombreRecursos[index].get('nombre')
                                descipcionRecurso = descipcionRecursos[index].get('descripcion')
                                tipoRecurso = tipoRecursos[index].get('tipo')
                                observacionesRecurso = observacionesRecursos[index].get('observaciones')
                                fotosRecurso = fotosRecursos[index].get('images')
                                html += '<div class="itinerarioRuta">'
                                html += '<div class="left-col-ruta"></div>'
                                html += '<div class="right-col-ruta">'
                                duracion = '0'
                                try:
                                    duracion = str(int(duracionSegmentos[duracionIndex] * 60))
                                    html += '<hr class="my-5"><span class="travel-time"><i class="fa fa-car" aria-hidden="true"></i>  ' + str(
                                        int(duracionSegmentos[duracionIndex] * 60)) + ' minutos</span>'
                                except:
                                    html += ''
                                html += '</div>'
                                html += '</div>'
                                html += '<div class="itinerario">'
                                html += '<div class="contenidoVisita">'
                                html += '<div class="left-col">'
                                hora = nuevoDiaInicio + relativedelta(hours=+float(acumulacionTiempo))
                                horaConDesplazamiento = hora + relativedelta(
                                    minutes=+int(duracionSegmentos[duracionIndex]))

                                duracionIndex+=1
                                try:
                                    acumulacionTiempo = tiempoRecurso + acumulacionTiempo + Decimal(
                                        duracionSegmentos[duracionIndex])
                                except:
                                    acumulacionTiempo = 0
                                html += '<p class="font-weight-bold dark-grey-text"><mdb-icon far icon="clock" class="pr-2"</mdb-icon> ' + str(horaConDesplazamiento.time()) + '</p>'
                                html += '</div>'
                                html += '<div class="row">'
                                html += '<div class="col-lg-5">'
                                html += '<div class="view overlay rounded z-depth-2 mb-lg-0 mb-4 waves-light" mdbWavesEffect><img class="img-fluid" src="https://mdbootstrap.com/img/Photos/Others/img (28).jpg"/></div>'
                                html += '</div>'
                                html += '<div class="col-lg-7">'
                                html += '<a href="#!" class="indigo-text"><h6 class="font-weight-bold mb-3"><mdb-icon fas icon="suitcase" class="pr-2"></mdb-icon>Travels</h6></a>'
                                html += '<h3 class="font-weight-bold mb-3"><strong>' + nombreRecurso + '</strong></h3>'
                                html += '<p>' + descipcionRecurso + '</p>'
                                html += '<p><strong>Tiempo de visita estimado:</strong> ' + str(tiempoRecurso) + ' h</p>'
                                html += '<button type="button" mdbBtn color="primary" mdbWavesEffect>Primary</button>'
                                html += '</div>'
                                html += '</div>'
                                html += '</div>'
                                html += '</div>'
                                html += '<div class="line-between"></div>'
                                itemsPlan.append([str(recursoIndex),duracion,str(horaConDesplazamiento.time()),nombreRecurso,descipcionRecurso,str(tiempoRecurso),tipoRecurso,observacionesRecurso,imagenesRecursos[index]])
                                recursoIndex = recursoIndex + 1
                        html += '</div>'
                        plan.append({str(fechaSiguienteSinHora):itemsPlan})
                        # eliminamos los recursos que ya hemos usado
                        del imagenesRecursos[0:recursos]
                        del tiempos[0:recursos]
                        del nombreRecursos[0:recursos]
                        del descipcionRecursos[0:recursos]
                        del tipoRecursos[0:recursos]
                        del observacionesRecursos[0:recursos]
                        del fotosRecursos[0:recursos]
                    else:
                        print('inicio: '+ str(nuevoDiaInicio))
                        for i in range(horasDiarias):
                            horasUtiles +=1
                            print(nuevoDiaInicio + relativedelta(hours=+(i+1)))
                        print('Horas dia 2:' + str(horasDiarias))
                        html += '<div class="dayBlock">'
                        html += '<div class="dia-container">'
                        html += '<p class="font-weight-bold dark-grey-text">'+str(fechaSiguienteSinHora)+'</p><hr class="my-5">'
                        html += '</div>'
                        html += '<div class="line-between"></div>'
                        acumulacionTiempo = 0
                        recursos = 0
                        try:
                            acumulacionTiempo = acumulacionTiempo + Decimal(duracionSegmentos[duracionIndex])
                        except:
                            acumulacionTiempo = 0
                        itemsPlan = []
                        for index, tiempo in enumerate(tiempos):
                            tiempoRecurso = tiempo.get('tiempo')
                            if acumulacionTiempo <= horasDiarias:
                                recursos += 1
                                nombreRecurso = nombreRecursos[index].get('nombre')
                                descipcionRecurso = descipcionRecursos[index].get('descripcion')
                                tipoRecurso = tipoRecursos[index].get('tipo')
                                observacionesRecurso = observacionesRecursos[index].get('observaciones')
                                fotosRecurso = fotosRecursos[index].get('images')
                                html += '<div class="itinerarioRuta">'
                                html += '<div class="left-col-ruta"></div>'
                                html += '<div class="right-col-ruta">'
                                duracion = '0'
                                try:
                                    duracion = str(int(duracionSegmentos[duracionIndex] * 60))
                                    html += '<hr class="my-5"><span class="travel-time"><i class="fa fa-car" aria-hidden="true"></i>  ' + str(
                                        int(duracionSegmentos[duracionIndex] * 60)) + ' minutos</span>'
                                except:
                                    html += ''
                                html += '</div>'
                                html += '</div>'
                                html += '<div class="itinerario">'
                                html += '<div class="contenidoVisita">'
                                html += '<div class="left-col">'
                                hora = nuevoDiaInicio + relativedelta(hours=+float(acumulacionTiempo))
                                horaConDesplazamiento = hora + relativedelta(
                                    minutes=+int(duracionSegmentos[duracionIndex]))

                                duracionIndex+=1
                                try:
                                    acumulacionTiempo = tiempoRecurso + acumulacionTiempo + Decimal(
                                        duracionSegmentos[duracionIndex])
                                except:
                                    acumulacionTiempo = 0
                                html += '<p class="font-weight-bold dark-grey-text"><mdb-icon far icon="clock" class="pr-2"</mdb-icon> ' + str(horaConDesplazamiento.time()) + '</p>'
                                html += '</div>'
                                html += '<div class="row">'
                                html += '<div class="col-lg-5">'
                                html += '<div class="view overlay rounded z-depth-2 mb-lg-0 mb-4 waves-light" mdbWavesEffect><img class="img-fluid" src="https://mdbootstrap.com/img/Photos/Others/img (28).jpg"/></div>'
                                html += '</div>'
                                html += '<div class="col-lg-7">'
                                html += '<a href="#!" class="indigo-text"><h6 class="font-weight-bold mb-3"><mdb-icon fas icon="suitcase" class="pr-2"></mdb-icon>Travels</h6></a>'
                                html += '<h3 class="font-weight-bold mb-3"><strong>' + nombreRecurso + '</strong></h3>'
                                html += '<p>' + descipcionRecurso + '</p>'
                                html += '<p><strong>Tiempo de visita estimado:</strong> ' + str(tiempoRecurso) + ' h</p>'
                                html += '<button type="button" mdbBtn color="primary" mdbWavesEffect>Primary</button>'
                                html += '</div>'
                                html += '</div>'
                                html += '</div>'
                                html += '</div>'
                                html += '<div class="line-between"></div>'
                                itemsPlan.append([str(recursoIndex),duracion,str(horaConDesplazamiento.time()),nombreRecurso,descipcionRecurso,str(tiempoRecurso),tipoRecurso,observacionesRecurso,imagenesRecursos[index]])
                                recursoIndex = recursoIndex + 1
                        html += '</div>'
                        plan.append({str(fechaSiguienteSinHora):itemsPlan})
                        # eliminamos los recursos que ya hemos usado
                        del imagenesRecursos[0:recursos]
                        del tiempos[0:recursos]
                        del nombreRecursos[0:recursos]
                        del descipcionRecursos[0:recursos]
                        del tipoRecursos[0:recursos]
                        del observacionesRecursos[0:recursos]
                        del fotosRecursos[0:recursos]

                #dias restantes
                if numeroDias > 2:
                    for j in range(numeroDias-2):
                        fechaSiguienteSinHora = fechaSiguienteSinHora + relativedelta(days=+1)
                        nuevoDiaInicio = nuevoDiaInicio + relativedelta(days=+1, hour=Inicial)
                        nuevoDiaFin = nuevoDiaInicio + relativedelta(hour=Final)
                        # comprobamos si la fecha coincide con el ultimo dia
                        comprobarUltimoDia = fechaSalidaSinHora - fechaSiguienteSinHora
                        if comprobarUltimoDia.days <= 0:
                            horasDiarias = fechaSalida - nuevoDiaInicio
                            horasDiarias = horasDiarias.seconds
                            horasDiarias = horasDiarias // 3600
                            print('inicio: '+ str(nuevoDiaInicio))
                            for i in range(horasDiarias):
                                horasUtiles +=1
                                print(nuevoDiaInicio + relativedelta(hours=+(i + 1)))
                            print('Horas dia ' +str(j+3) +': '+ str(horasDiarias))
                            print('fin')
                            html += '<div class="dayBlock">'
                            html += '<div class="dia-container">'
                            html += '<p class="font-weight-bold dark-grey-text">'+str(fechaSiguienteSinHora)+'</p><hr class="my-5">'
                            html += '</div>'
                            html += '<div class="line-between"></div>'
                            acumulacionTiempo = 0
                            recursos = 0
                            try:
                                acumulacionTiempo = acumulacionTiempo + Decimal(duracionSegmentos[duracionIndex])
                            except:
                                acumulacionTiempo = 0
                            itemsPlan = []
                            for index, tiempo in enumerate(tiempos):
                                tiempoRecurso = tiempo.get('tiempo')
                                if acumulacionTiempo <= horasDiarias:
                                    recursos += 1
                                    nombreRecurso = nombreRecursos[index].get('nombre')
                                    descipcionRecurso = descipcionRecursos[index].get('descripcion')
                                    tipoRecurso = tipoRecursos[index].get('tipo')
                                    observacionesRecurso = observacionesRecursos[index].get('observaciones')
                                    fotosRecurso = fotosRecursos[index].get('images')
                                    html += '<div class="itinerarioRuta">'
                                    html += '<div class="left-col-ruta"></div>'
                                    html += '<div class="right-col-ruta">'
                                    duracion = '0'
                                    try:
                                        duracion = str(int(duracionSegmentos[duracionIndex] * 60))
                                        html += '<hr class="my-5"><span class="travel-time"><i class="fa fa-car" aria-hidden="true"></i>  ' + str(
                                            int(duracionSegmentos[duracionIndex] * 60)) + ' minutos</span>'
                                    except:
                                        html += ''
                                    html += '</div>'
                                    html += '</div>'
                                    html += '<div class="itinerario">'
                                    html += '<div class="contenidoVisita">'
                                    html += '<div class="left-col">'
                                    hora = nuevoDiaInicio + relativedelta(hours=+float(acumulacionTiempo))
                                    horaConDesplazamiento = hora + relativedelta(
                                        minutes=+int(duracionSegmentos[duracionIndex]))

                                    duracionIndex+=1
                                    try:
                                        acumulacionTiempo = tiempoRecurso + acumulacionTiempo + Decimal(
                                            duracionSegmentos[duracionIndex])
                                    except:
                                        acumulacionTiempo = 0
                                    html += '<p class="font-weight-bold dark-grey-text"><mdb-icon far icon="clock" class="pr-2"</mdb-icon> ' + str(horaConDesplazamiento.time()) + '</p>'
                                    html += '</div>'
                                    html += '<div class="row">'
                                    html += '<div class="col-lg-5">'
                                    html += '<div class="view overlay rounded z-depth-2 mb-lg-0 mb-4 waves-light" mdbWavesEffect><img class="img-fluid" src="https://mdbootstrap.com/img/Photos/Others/img (28).jpg"/></div>'
                                    html += '</div>'
                                    html += '<div class="col-lg-7">'
                                    html += '<a href="#!" class="indigo-text"><h6 class="font-weight-bold mb-3"><mdb-icon fas icon="suitcase" class="pr-2"></mdb-icon>Travels</h6></a>'
                                    html += '<h3 class="font-weight-bold mb-3"><strong>' + nombreRecurso + '</strong></h3>'
                                    html += '<p>' + descipcionRecurso + '</p>'
                                    html += '<p><strong>Tiempo de visita estimado:</strong> ' + str(tiempoRecurso) + ' h</p>'
                                    html += '<button type="button" mdbBtn color="primary" mdbWavesEffect>Primary</button>'
                                    html += '</div>'
                                    html += '</div>'
                                    html += '</div>'
                                    html += '</div>'
                                    html += '<div class="line-between"></div>'
                                    itemsPlan.append([str(recursoIndex),duracion,str(horaConDesplazamiento.time()),nombreRecurso,descipcionRecurso,str(tiempoRecurso),tipoRecurso,observacionesRecurso,imagenesRecursos[index]])
                                    recursoIndex = recursoIndex + 1
                            html += '</div>'
                            plan.append({str(fechaSiguienteSinHora):itemsPlan})
                            # eliminamos los recursos que ya hemos usado
                            del imagenesRecursos[0:recursos]
                            del tiempos[0:recursos]
                            del nombreRecursos[0:recursos]
                            del descipcionRecursos[0:recursos]
                            del tipoRecursos[0:recursos]
                            del observacionesRecursos[0:recursos]
                            del fotosRecursos[0:recursos]

                        else:
                            print('inicio: '+ str(nuevoDiaInicio))
                            for i in range(horasDiarias):
                                horasUtiles +=1
                                print(nuevoDiaInicio + relativedelta(hours=+(i + 1)))
                            print('Horas dia ' + str(j + 3) +': '+ str(horasDiarias))
                            html += '<div class="dayBlock">'
                            html += '<div class="dia-container">'
                            html += '<p class="font-weight-bold dark-grey-text">'+str(fechaSiguienteSinHora)+'</p><hr class="my-5">'
                            html += '</div>'
                            html += '<div class="line-between"></div>'
                            acumulacionTiempo = 0
                            recursos = 0
                            try:
                                acumulacionTiempo = acumulacionTiempo + Decimal(duracionSegmentos[duracionIndex])
                            except:
                                acumulacionTiempo = 0
                            itemsPlan = []
                            for index, tiempo in enumerate(tiempos):
                                tiempoRecurso = tiempo.get('tiempo')
                                if acumulacionTiempo <= horasDiarias:
                                    recursos += 1
                                    nombreRecurso = nombreRecursos[index].get('nombre')
                                    descipcionRecurso = descipcionRecursos[index].get('descripcion')
                                    tipoRecurso = tipoRecursos[index].get('tipo')
                                    observacionesRecurso = observacionesRecursos[index].get('observaciones')
                                    fotosRecurso = fotosRecursos[index].get('images')
                                    html += '<div class="itinerarioRuta">'
                                    html += '<div class="left-col-ruta"></div>'
                                    html += '<div class="right-col-ruta">'
                                    duracion = '0'
                                    try:
                                        duracion = str(int(duracionSegmentos[duracionIndex] * 60))
                                        html += '<hr class="my-5"><span class="travel-time"><i class="fa fa-car" aria-hidden="true"></i>  ' + str(
                                            int(duracionSegmentos[duracionIndex] * 60)) + ' minutos</span>'
                                    except:
                                        html += ''
                                    html += '</div>'
                                    html += '</div>'
                                    html += '<div class="itinerario">'
                                    html += '<div class="contenidoVisita">'
                                    html += '<div class="left-col">'
                                    hora = nuevoDiaInicio + relativedelta(hours=+float(acumulacionTiempo))
                                    horaConDesplazamiento = hora + relativedelta(
                                        minutes=+int(duracionSegmentos[duracionIndex]))

                                    duracionIndex+=1
                                    try:
                                        acumulacionTiempo = tiempoRecurso + acumulacionTiempo + Decimal(
                                            duracionSegmentos[duracionIndex])
                                    except:
                                        acumulacionTiempo = 0
                                    html += '<p class="font-weight-bold dark-grey-text"><mdb-icon far icon="clock" class="pr-2"</mdb-icon> ' + str(horaConDesplazamiento.time()) + '</p>'
                                    html += '</div>'
                                    html += '<div class="row">'
                                    html += '<div class="col-lg-5">'
                                    html += '<div class="view overlay rounded z-depth-2 mb-lg-0 mb-4 waves-light" mdbWavesEffect><img class="img-fluid" src="https://mdbootstrap.com/img/Photos/Others/img (28).jpg"/></div>'
                                    html += '</div>'
                                    html += '<div class="col-lg-7">'
                                    html += '<a href="#!" class="indigo-text"><h6 class="font-weight-bold mb-3"><mdb-icon fas icon="suitcase" class="pr-2"></mdb-icon>Travels</h6></a>'
                                    html += '<h3 class="font-weight-bold mb-3"><strong>' + nombreRecurso + '</strong></h3>'
                                    html += '<p>' + descipcionRecurso + '</p>'
                                    html += '<p><strong>Tiempo de visita estimado:</strong> ' + str(tiempoRecurso) + ' h</p>'
                                    html += '<button type="button" mdbBtn color="primary" mdbWavesEffect>Primary</button>'
                                    html += '</div>'
                                    html += '</div>'
                                    html += '</div>'
                                    html += '</div>'
                                    html += '<div class="line-between"></div>'
                                    itemsPlan.append([str(recursoIndex),duracion,str(horaConDesplazamiento.time()),nombreRecurso,descipcionRecurso,str(tiempoRecurso),tipoRecurso,observacionesRecurso,imagenesRecursos[index]])
                                    recursoIndex = recursoIndex + 1
                            html += '</div>'
                            plan.append({str(fechaSiguienteSinHora):itemsPlan})
                            # eliminamos los recursos que ya hemos usado
                            del imagenesRecursos[0:recursos]
                            del tiempos[0:recursos]
                            del nombreRecursos[0:recursos]
                            del descipcionRecursos[0:recursos]
                            del tipoRecursos[0:recursos]
                            del observacionesRecursos[0:recursos]
                            del fotosRecursos[0:recursos]
                html += '</div>'
        html += '</div>'
        html += '</div>'
        #html += '</div>'
        data = 'no data'
        recursos_arr=json.dumps(recursos_arr, cls=DjangoJSONEncoder)
        recursosNombres_arr = json.dumps(recursosNombres_arr, cls=DjangoJSONEncoder)
        context = {
            'html': html,
            'data':geojson,
            'recursos':recursos_arr,
            'recursosNombres':recursosNombres_arr,
            'plan':plan
        }
        return Response(context, status=status.HTTP_200_OK)
