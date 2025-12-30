from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Salida(models.Model):
    MES_CHOICES = [
        ('enero', 'Enero'),
        ('febrero', 'Febrero'),
        ('marzo', 'Marzo'),
        ('abril', 'Abril'),
        ('mayo', 'Mayo'),
        ('junio', 'Junio'),
        ('julio', 'Julio'),
        ('agosto', 'Agosto'),
        ('septiembre', 'Septiembre'),
        ('octubre', 'Octubre'),
        ('noviembre', 'Noviembre'),
        ('diciembre', 'Diciembre'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mes = models.CharField(max_length=20, choices=MES_CHOICES)
    lugar = models.CharField(max_length=200)

    puntualidad = models.IntegerField()
    creatividad = models.IntegerField()
    ambiente = models.IntegerField()
    repetir = models.IntegerField()

    puntaje_total = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.mes}"

