from rest_framework import serializers
from .models import Usuario, Salida

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre']

class SalidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salida
        fields = [
            'id', 'usuario', 'mes', 'lugar',
            'puntualidad', 'creatividad', 'ambiente', 'repetir',
            'puntaje_total', 'created_at'
        ]

