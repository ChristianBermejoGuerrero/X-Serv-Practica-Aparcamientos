from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from parkingapp.xmlparser import update
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context, RequestContext, Template
from django.contrib.auth.models import User
from parkingapp.models import Aparcamiento, PaginaUsuario, AparcSelect, Distrito, Comentario
import time

globAcc = False

# Post.objects.order_by('created_date')
##################### 5 aparcamientos mas comentados y TEMPLATES ###############################
@csrf_exempt
def showPrincipal(request):
    global globAcc
    userlist = User.objects.all()
    pageuserlist = PaginaUsuario.objects.all()
    if len(userlist) != len(pageuserlist):
        for user in userlist:
            paginausuario = PaginaUsuario(usuario=user,titulo=("Pagina de " + user.username))
            paginausuario.save()
        pageuserlist = PaginaUsuario.objects.all()
    aparclist = Aparcamiento.objects.all()
    aparclistAcc = Aparcamiento.objects.all().filter(accesibilidad=1)
    respuesta = "<h2>BASE DE DATOS</h2>"
    if request.method == "POST" and globAcc == False:
        globAcc = True
    elif request.method == "POST" and globAcc == True:
        globAcc = False
    respuesta += '<form action="" method="POST">'
    if globAcc == False:
        respuesta += '<input type="submit" value="Aparcamientos Accesibles"></form>'
        if len(aparclist) != 0:
            for aparc in aparclist:
                respuesta+="<h4><li> | " + aparc.nombre + "</li></h4>"
        else :
            respuesta += "NO HAY APARCAMIENTOS CARGADOS POR FAVOR VE A /uploadxml."
    else:
        respuesta += '<input type="submit" value="Todos los aparcamientos"></form>'
        if len(aparclistAcc) != 0 and len(aparclist) != 0:
            for aparcAcc in aparclistAcc:
                    respuesta+="<h4><li> | " + aparcAcc.nombre + "</li></h4>"
        else :
            respuesta += "NO HAY APARCAMIENTOS DISPONIBLES AHORA MISMO."
    if len(pageuserlist) != 0:
        respuesta += "<h2>PAGINAS DE USUARIO</h2>"
        for pageuser in pageuserlist:
            respuesta+="<h4><li>" + pageuser.usuario.username + " | "
            respuesta+= "<a href='" + pageuser.usuario.username + "'>" + pageuser.titulo + "</a></li></h4>"
    else :
        respuesta += "NO TENEMOS PAGINAS DE USUARIO. CREA USUARIOS POR FAVOR."
    if request.user.is_authenticated():
        respuesta += "ENHORABUENA ESTAS REGISTRADO COMO " + request.user.username
    else:
        respuesta += "<h3> Not logged in. Log in here >>><a href='/login'>LOGIN</a> </h3>"
    return HttpResponse(respuesta)

##################### APARCAMIENTOS DE 5 EN 5, CUANDO LLEGA POST DE CSS y TEMPLATES ######################
@csrf_exempt
def showUserpage(request,nombre):
    try:
        useraux = User.objects.get(username=nombre)
        pageuser = PaginaUsuario.objects.get(usuario=useraux)
        aparclistSelect = AparcSelect.objects.all().filter(pagUsuario=pageuser)
        respuesta = pageuser.titulo
        if len(aparclistSelect) != 0:
            respuesta += "<h4>APARCAMIENTOS SELECCIONADOS</h4>"
            for select in aparclistSelect:
                respuesta += "Nombre Aparcamiento: " + select.aparcamiento.nombre
                direccion = select.aparcamiento.clasevial + " " + select.aparcamiento.nombrevia
                direccion += " " + select.aparcamiento.numvia
                respuesta += "<br>Direccion aparcamiento: " + direccion
                respuesta += "<br><a href='" + select.aparcamiento.link + "'>" + "Mas Informacion" + "</a>"
                aux = (str(select.fechaSelect))
                aux = aux[0:aux.find(".")]
                respuesta += "<br>Fecha de seleccion: " + aux
    except PaginaUsuario.DoesNotExist:
        respuesta = "HAS INTRODUCIDO EL NOMBRE DEL USUARIO MAL O NO EXISTE."

    if request.user.is_authenticated():
        respuesta += ". <br><br>ENHORABUENA ESTAS REGISTRADO"
        respuesta += '<form action="" method="POST">'
        respuesta += 'Nuevo titulo de tu pagina personal: <input type="text" name="titulo">'
        respuesta += '<input type="submit" value="Enviar Titulo" name="nuevotitulo"></form>'
        respuesta += '<form action="" method="POST">'
        respuesta += 'Nuevo tamaño de letra: <input type="text" name="nuevotamaño">'
        respuesta += '<br>Nuevo color de fondo: <input type="text" name="nuevocolor">'
        respuesta += '<input type="submit" value="Enviar CSS" name="nuevoCSS"></form>'
        if request.method == "POST" and request.POST.get("nuevoCSS", "") == 'Enviar CSS':
            print("hola")
            return HttpResponseRedirect("/" + nombre)
        if request.method == "POST" and request.POST.get("nuevotitulo", "") == 'Enviar Titulo':
            nuevotitulo = request.POST['titulo']
            useraux = User.objects.get(username=request.user.username)
            pageuser = PaginaUsuario.objects.get(usuario=useraux)
            pageuser.titulo = nuevotitulo
            pageuser.save()
            return HttpResponseRedirect("/" + nombre)

    return HttpResponse(respuesta)

@csrf_exempt
def showAllParkings(request):
    respuesta = '<form action="" method="POST">'
    respuesta += 'Filtrar por distrito del aparcamiento: <input type="text" name="distrito">'
    respuesta += '<input type="submit" value="Enviar" name="distrito a filtrar"></form>'
    if request.method == "POST":
        distritofilt = request.POST['distrito'].upper()
        respuesta += "<h2>APARCAMIENTOS DEL DISTRITO: " + distritofilt + "</h2>"
        distritoaux = Distrito.objects.get(nombre=distritofilt)
        aparclist = Aparcamiento.objects.all().filter(distrito=distritoaux)
        if len(aparclist) != 0:
            for aparc in aparclist:
                respuesta +="<h4><li>" + aparc.nombre + " | "
                respuesta +="<a href='/aparcamientos/" + str(aparc.id) + "'>Pagina del aparcamiento</a></li></h4>"
    else:
        respuesta += "<h2>TODOS LOS APARCAMIENTOS</h2>"
        aparclist = Aparcamiento.objects.all()
        if len(aparclist) != 0:
            for aparc in aparclist:
                respuesta +="<h4><li>" + aparc.nombre + " | "
                respuesta +="<a href='/aparcamientos" + str(aparc.id) + "'>Pagina del aparcamiento</a></li></h4>"

    return HttpResponse(respuesta)


@csrf_exempt
def showOneParking(request,identificador):
    aparcaux = Aparcamiento.objects.get(id=identificador)
    respuesta = "Nombre: " + aparcaux.nombre
    direccion = aparcaux.clasevial + " " + aparcaux.nombrevia + " " + aparcaux.numvia
    respuesta += "<br>Direccion: " + direccion
    respuesta += "<br><a href='" + aparcaux.link + "'>Pagina Oficial del aparcamiento</a>"
    respuesta += "<br>Latitud: " + str(aparcaux.latitud) + " | Longitud: " + str(aparcaux.longitud)
    respuesta += "<br>Descripcion: " + aparcaux.descripcion
    respuesta += "<br>Distrito: " + aparcaux.distrito.nombre + " | Barrio: " + aparcaux.barrio
    commentlist = Comentario.objects.all().filter(aparcamiento=aparcaux)
    if  aparcaux.accesibilidad == 1:
        respuesta += "<br>Accesibilidad: Plazas disponibles"
    else:
        respuesta += "<br>Accesibilidad: NO disponible"
    if aparcaux.telefono == None or aparcaux.email == None:
        respuesta += "<br>Datos de contacto: N/S"
    else:
        respuesta += "<br>Datos de contacto:"
        respuesta += "<li>Telefono: " + aparcaux.telefono + "</li>"
        respuesta += "<li>Email: " + aparcaux.email + "</li>"
    respuesta += "<br>COMENTARIOS: " #text y aparcamiento
    if len(commentlist) != 0:
        for comment in commentlist:
            respuesta +="</br>" + comment.text
    if request.user.is_authenticated():
        respuesta += "<br>ENHORABUENA ESTAS REGISTRADO como " + request.user.username
        respuesta += "<br>Deja tu comentario sobre este aparcamiento: "
        respuesta += '<form action="" method="POST">'
        respuesta += 'Comentario: <input type="text" name="nuevocomentario">'
        respuesta += '<input type="submit" value="Enviar Comentario" name="comentario"></form>'
        respuesta += "<br>Selecciona este aparcamiento para que aparezca en tu pagina personal"
        respuesta += '<form action="" method="POST">'
        respuesta += '<br><input type="submit" value="Seleccionar aparcamiento" name="seleccionar"></form>'
        if request.method == "POST" and request.POST.get("seleccionar", "") == 'Seleccionar aparcamiento':
            pageuser = PaginaUsuario.objects.get(usuario=request.user)
            select = AparcSelect(usuario=request.user,pagUsuario=pageuser,aparcamiento=aparcaux)
            select.save()
            return HttpResponseRedirect("/aparcamientos/" + identificador)
        if request.method == "POST" and request.POST.get("comentario", "") == 'Enviar Comentario':
            comment = request.POST['nuevocomentario']
            nuevocomentario = Comentario(text=comment,aparcamiento=aparcaux)
            nuevocomentario.save()
            if aparcaux.numcomments == None:
                aparcaux.numcomments = 1
            else:
                aparcaux.numcomments = aparcaux.numcomments + 1
            aparcaux.save()
            return HttpResponseRedirect("/aparcamientos/" + identificador)

    return HttpResponse(respuesta)

# def userxml(request,nombre):
#     return print("hola")
#
# def about(request):
#     return print("hola")

def logout(request):
    #redirigir a /admin/logout
    return redirect('/admin/logout/')

def uploadxml(request):
    update()
    return redirect('/')
