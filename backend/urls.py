from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('mis_salidas.urls')),  # Todos los endpoints de la app
]