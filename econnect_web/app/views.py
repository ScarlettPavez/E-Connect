from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Evento, Lugar
from .forms import AddLugarForm, AddEventoForm, AddEventoAdminForm
from django.contrib import messages
from django.http import HttpResponse, FileResponse
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator


def Lugarpdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    Lugares = Lugar.objects.all()
    lines = []
    for lugar in Lugares:
        lines.append(lugar.Nombre)
        lines.append(lugar.dirección)
        lines.append(lugar.código_zip)
        lines.append(lugar.teléfono)
        lines.append(lugar.web)
        lines.append(lugar.email)
        lines.append("===================================")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='Lugar.pdf')


def Lugarcsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Lugares.csv'
    writer = csv.writer(response)
    lugares = Lugar.objects.all()
    writer.writerow(['Lugar Nombre', 'dirección', 'Zip Code', 'teléfono', 'Website', 'Email dirección'])
    for lugar in lugares:
        writer.writerow([lugar.Nombre, lugar.dirección, lugar.código_zip, lugar.teléfono, lugar.web, lugar.email])
    
    return response


def Lugartext(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition']='attachment; fileNombre=Lugars.txt'
    Lugars = Lugar.objects.all()
    lines = []
    for lugar in Lugars:
        lines.append(f'{lugar.Nombre}\n {lugar.dirección}\n {lugar.código_zip}\n {lugar.teléfono}\n {lugar.web}\n {lugar.email}\n\n\n')
    
    response.writelines(lines)
    return response


# Create your views here.
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    Nombre = 'Scarlett'
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    

    cal = HTMLCalendar().formatmonth(
        year,
        month_number
    )

    now = datetime.now()
    current_year = now.year

    time = now.strftime('%H:%M:%S')
    
    return render(request, 'home.html', {
        'Nombre':Nombre, 
        'year':year, 
        'month':month, 
        'month_number':month_number,
        'cal':cal,
        'current_year':current_year,
        'time':time,
        })


def Eventoview(request):
    Eventos = Evento.objects.all().order_by('Nombre')
    return render(request, 'Eventos.html', {'Eventos':Eventos})


def addLugarview(request):
    form = AddLugarForm()
    if request.method == 'POST':
        form = AddLugarForm(request.POST, request.FILES)
        if form.is_valid():
            Lugar = form.save(commit=False)
            Lugar.owner = request.user.id
            Lugar.save()
            #form.save()
            messages.success(request, "El lugar del evento ha sido guardado")
            return redirect('addLugar')
            
    else:
        form =AddLugarForm()

    return render(request, 'agregar_lugar.html', {'form':form})


def Lugarlistview(request):
    p = Paginator(Lugar.objects.all(), 1)
    page = request.GET.get('page')
    Lugars = p.get_page(page)
    nums = "a" * Lugars.paginator.num_pages
    return render(request, 'lugar_lista.html', {'Lugars':Lugars, 'nums':nums})


def Lugardetailview(request, Lugar_id):
    Lugars = Lugar.objects.get(pk=Lugar_id)
    return render(request, 'detalle_lugar.html', {'Lugars':Lugars})


def Eventodetailview(request, Evento_id):
    evento = Evento.objects.get(pk=Evento_id)
    return render(request, 'detalles_evento.html', {'Evento':evento})


def searchLugarview(request):
    if request.method == "POST":
        searched = request.POST['searched']
        Lugars = Lugar.objects.filter(Nombre__contains=searched)
    return render(request, 'buscar_lugar.html', {'searched':searched, 'Lugars':Lugars})


def upfechaLugarview(request, Lugar_id):
    Lugars = Lugar.objects.get(pk=Lugar_id)
    form = AddLugarForm(request.POST or None, request.FILES or None, instance=Lugars)
    if form.is_valid():
        form.save()
        return redirect('Lugarlist')
    return render(request, 'actualizar_lugar.html', {'form':form})


def deleteLugarview(request, Lugar_id):
    Lugars = Lugar.objects.get(pk=Lugar_id)
    if request.method == "POST":
        Lugars.delete()
        return redirect('Lugarlist')

    return render(request, 'eliminar_lugar.html', {'Lugars':Lugars})


def addEventoview(request):
    if request.method == "POST":
        if request.user.is_superuser:
            form = AddEventoAdminForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('addEvento')
        else:
            form = AddEventoForm(request.POST)
            if form.is_valid():
                Evento = form.save(commit=False)
                Evento.gestor = request.user
                Evento.save()
                return redirect('addEvento')
    else:
        if request.user.is_superuser:
            form = AddEventoAdminForm()
        else:
            form = AddEventoForm()
    return render(request, 'agregar_evento.html', {'form':form})


def editEventoview(request, Evento_id):
    Eventos = Evento.objects.get(pk=Evento_id)
    if request.user.is_superuser:
        form = AddEventoAdminForm(request.POST or None, instance=Eventos)
    else:
        form = AddEventoForm(request.POST or None, instance=Eventos)
    
    if form.is_valid():
        form.save()
        return redirect('Eventos')
        
    return render(request, 'editar_evento.html', {'form':form})


def searchEventoview(request):
    if request.method == "POST":
        searched = request.POST['searched']
        Eventos = Evento.objects.filter(name__contains=searched)
        
    return render(request, 'buscar_evento.html', {'Eventos':Eventos})


def adminpprovalview(request):
    Eventos = Evento.objects.all()
    Lugars = Lugar.objects.all()
    Lugar_number = len(Lugars)
    Evento_number = len(Eventos)

    if request.method == "POST":
        id_list = request.POST.getlist('boxes')
        Eventos.upfecha(approved=False)
        for x in id_list:
            Evento.objects.filter(pk=int(x)).upfecha(approved=True)
        return redirect('Eventos')
    return render(request, 'adminapproval.html', {'Eventos':Eventos, 'Lugar_number':Lugar_number, 'Evento_number':Evento_number})



def EventoLugarcategoryview(request, Lugar_id):
    lugar = Lugar.objects.get(pk=Lugar_id)
    eventos = Evento.objects.filter(Lugar = lugar)
    return render(request, 'evento_lugar_categoria.html', {'Eventos':eventos})