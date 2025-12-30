from rest_framework import viewsets
from .models import Usuario, Salida
from .serializers import UsuarioSerializer, SalidaSerializer
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg,  Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]

class ResultadosView(APIView):
    def get(self, request):
        resultados = (
            Salida.objects
            .values('mes')
            .annotate(
                total_puntos=Sum('puntaje_total'),
                total_votos=Count('id')
            )
            .order_by('-total_puntos')
        )

        return Response(resultados)

class SalidaViewSet(viewsets.ModelViewSet):
    queryset = Salida.objects.all()
    serializer_class = SalidaSerializer


def meses_votados(request):
    usuario_id = request.GET.get('usuario_id')

    if not usuario_id:
        return JsonResponse(
            {"error": "usuario_id requerido"},
            status=400
        )

    meses = list(
        Salida.objects
        .filter(usuario_id=usuario_id)
        .values_list('mes', flat=True)
        .distinct()
    )

    return JsonResponse({"meses": meses})

@csrf_exempt
def limpiar_todo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
            confirmacion = data.get('confirmar', False)
            
            if not confirmacion:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Se requiere confirmación. Envía {"confirmar": true}'
                }, status=400)
            
            with connection.cursor() as cursor:
                # TABLAS ESPECÍFICAS DE TU APP
                tablas_a_limpiar = [
                    'mis_salidas_salida',    # Votos/salidas
                    'mis_salidas_usuario',   # Usuarios
                    'salidas_salida',        # Tabla vacía pero por si acaso
                    'salidas_usuario'        # Tabla vacía pero por si acaso
                ]
                
                total_eliminados = 0
                tablas_limpiadas = []
                
                for tabla in tablas_a_limpiar:
                    cursor.execute(f"DELETE FROM {tabla}")
                    eliminados = cursor.rowcount
                    if eliminados > 0:
                        total_eliminados += eliminados
                        tablas_limpiadas.append(tabla)
                        print(f"✅ {tabla}: {eliminados} registros eliminados")
                
                # Resetear los IDs autoincrementales
                cursor.execute("DELETE FROM sqlite_sequence")
                
                # Opcional: Vaciar sesiones de Django también
                cursor.execute("DELETE FROM django_session")
            
            return JsonResponse({
                'status': 'success', 
                'message': f'Base de datos limpiada. {total_eliminados} registros eliminados.',
                'detalle': {
                    'registros_eliminados': total_eliminados,
                    'tablas_limpiadas': tablas_limpiadas,
                    'salidas_eliminadas': 'mis_salidas_salida (18)',
                    'usuarios_eliminados': 'mis_salidas_usuario (7)'
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error', 
        'message': 'Método no permitido. Usa POST.'
    }, status=405)