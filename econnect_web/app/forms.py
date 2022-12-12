from django import forms
from .models import Lugar, Evento


class AddLugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = ('Nombre', 'dirección', 'código_zip', 'teléfono', 'web', 'email', 'imagen')


        widgets = {
            'Nombre':forms.TextInput(attrs={'class':'form-control'}),
            'dirección':forms.TextInput(attrs={'class':'form-control'}),
            'código_zip':forms.TextInput(attrs={'class':'form-control'}),
            'teléfono':forms.TextInput(attrs={'class':'form-control'}),
            'web':forms.URLInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),

        }



class AddEventoAdminForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ('Nombre', 'Evento_fecha', 'Lugar', 'gestor', 'Descripción', 'Asistentes')


        widgets = {
            'Nombre':forms.TextInput(attrs={'class':'form-control'}),
            'Evento_fecha':forms.TextInput(attrs={'class':'form-control', 'placeholder':'YYYY-MM-DD HH:MM:SS'}),
            'Lugar':forms.Select(attrs={'class':'form-control'}),
            'gestor':forms.Select(attrs={'class':'form-control'}),
            'Descripción':forms.Textarea(attrs={'class':'form-control'}),
            'Asistentes':forms.SelectMultiple(attrs={'class':'form-control'}),

        }


class AddEventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ('Nombre', 'Evento_fecha', 'Lugar', 'Descripción', 'Asistentes')


        widgets = {
            'Nombre':forms.TextInput(attrs={'class':'form-control'}),
            'Evento_fecha':forms.TextInput(attrs={'class':'form-control', 'placeholder':'YYYY-MM-DD HH:MM:SS'}),
            'Lugar':forms.Select(attrs={'class':'form-control'}),
            'Descripción':forms.Textarea(attrs={'class':'form-control'}),
            'Asistentes':forms.SelectMultiple(attrs={'class':'form-control'}),

        }