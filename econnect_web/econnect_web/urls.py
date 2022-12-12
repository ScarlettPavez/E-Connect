from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('miembros/', include('django.contrib.auth.urls')),
    path('miembros/', include('miembros.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



#Admin Area Header
admin.site.site_header = "E-CONNECT"