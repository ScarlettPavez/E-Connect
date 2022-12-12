from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

# Create your models here.

class Lugar(models.Model):
    Nombre = models.CharField(max_length=150)
    dirección = models.CharField(max_length=150)
    código_zip = models.CharField(max_length=150)
    teléfono = models.CharField(max_length=10)
    web = models.URLField(max_length=50, blank=True)
    email = models.EmailField()
    owner = models.IntegerField(blank=False, default=1)
    imagen = models.ImageField(blank=True, null=True, upload_to='imagens/')


    def __str__(self):
        return self.Nombre


class eConnectUser(models.Model):
    primer_Nombre = models.CharField(max_length=100)
    apellido_Nombre = models.CharField(max_length=100)
    email = models.EmailField()


    def __str__(self):
        return self.primer_Nombre + ' ' + self.apellido_Nombre


class Evento(models.Model):
    Nombre = models.CharField(max_length=200)
    Evento_fecha = models.DateTimeField()
    Lugar = models.ForeignKey(Lugar, blank=True, null=True, on_delete=models.CASCADE)
    #Lugar = models.CharField(max_length=200)
    gestor = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    Descripción = models.TextField(blank=True)
    Asistentes = models.ManyToManyField(eConnectUser, blank=True)
    approved = models.BooleanField(default=False)


    def __str__(self):
        return self.Nombre


    @property
    def days_till(self):
        today = date.today()
        day_till = self.Evento_fecha.date() - today
        days_till_stripped = str(day_till).split(",", 1)[0]
        return days_till_stripped


    @property
    def is_past(self):
        today = date.today()
        if self.Evento_fecha.date() < today:
            thing = "Past"
        else:
            thing = "Future"
        return thing