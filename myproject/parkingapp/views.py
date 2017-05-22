from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from parkingapp.xmlparser import update
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context, RequestContext, Template
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from parkingapp.models import Aparcamiento, PaginaUsuario, AparcSelect, Distrito, Comentario

globAcc = False

##################### TEMPLATES ###############################
@csrf_exempt
def showPrincipal(request):
    global globAcc
    template = get_template('button.html')
    userlist = User.objects.all()
    pageuserlist = PaginaUsuario.objects.all()
    if len(userlist) != len(pageuserlist):
        for user in userlist:
            paginausuario = PaginaUsuario(usuario=user,titulo=("Pagina de " + user.username))
            paginausuario.save()
    pageuserlist = PaginaUsuario.objects.all()
    aparclist = Aparcamiento.objects.all()
    aparclistOrden = aparclist.exclude(numcomments=0).order_by('numcomments').reverse()[:5]
    aparclistAcc = Aparcamiento.objects.all().filter(accesibilidad=1)
    aparclistAccOrden = aparclistAcc.exclude(numcomments=0).order_by('numcomments').reverse()[:5]
    # tenemos que modificar las listas anteriores para poder pasarlas como contexto
    if request.method == "POST" and globAcc == False:
        globAcc = True
    elif request.method == "POST" and globAcc == True:
        globAcc = False
    c = RequestContext(request, {'globAcc':globAcc,
                                 'pageuserlist':pageuserlist,
                                 'aparclistOrden':aparclistOrden,
                                 'aparclistAccOrden':aparclistAccOrden})
    return HttpResponse(template.render(c))

##################### APARCAMIENTOS DE 5 EN 5, CUANDO LLEGA POST DE CSS y TEMPLATES ######################
@csrf_exempt
def showUserpage(request,nombre):
    template = get_template('userpage.html')
    try:
        useraux = User.objects.get(username=nombre)
        pageuser = PaginaUsuario.objects.get(usuario=useraux)
        aparclistSelect = AparcSelect.objects.all().filter(pagUsuario=pageuser)
        aparclistAccSelect = []
        for aparcSelect in aparclistSelect:
            if aparcSelect.aparcamiento.accesibilidad == 1:
                aparclistAccSelect.append(aparcSelect)

    except PaginaUsuario.DoesNotExist:
        respuesta = "HAS INTRODUCIDO EL NOMBRE DEL USUARIO MAL O NO EXISTE."
    if request.method == "POST":
        print(request)
    if request.method == "POST" and "tamaño" in request.POST and "color" in request.POST:
        print("hola")  ##################################################PROCESAR CSS
        return HttpResponseRedirect("/" + nombre)
    if request.method == "POST" and "nuevotitulo" in request.POST:
        print("hola1")
        nuevotitulo = request.POST['nuevotitulo']
        useraux = User.objects.get(username=request.user.username)
        pageuser = PaginaUsuario.objects.get(usuario=useraux)
        pageuser.titulo = nuevotitulo
        pageuser.save()
        return HttpResponseRedirect("/" + nombre)

    c = RequestContext(request, {'globAcc':globAcc,
                                 'aparclistSelect':aparclistSelect,
                                 'aparclistAccSelect':aparclistAccSelect})
    return HttpResponse(template.render(c))

@csrf_exempt
def showAllParkings(request):
    template = get_template('allAparcs.html')
    aparclist = Aparcamiento.objects.all()
    aparclistAcc = aparclist.filter(accesibilidad=1)
    if request.method == "POST":
        distritofilt = request.POST['distrito'].upper()
        distritoaux = Distrito.objects.get(nombre=distritofilt)
        aparclistFilt = aparclist.filter(distrito=distritoaux)
        aparclistAccFilt = aparclistFilt.filter(accesibilidad=1)
        c = RequestContext(request, {'globAcc':globAcc,
                                     'aparclist':aparclistFilt,
                                     'aparclistAcc':aparclistAccFilt})
    elif request.method == "GET":
        c = RequestContext(request, {'globAcc':globAcc,
                                     'aparclist':aparclist,
                                     'aparclistAcc':aparclistAcc})

    return HttpResponse(template.render(c))


@csrf_exempt
def showOneParking(request,identificador):
    aparcaux = Aparcamiento.objects.get(id=identificador)
    respuesta = "Nombre: " + aparcaux.nombre
    direccion = aparcaux.clasevial + " " + aparcaux.nombrevia + " "
    if aparcaux.numvia == None:
        respuesta += "<br>Direccion: " + direccion + "S/N"
    else:
        respuesta += "<br>Direccion: " + direccion + aparcaux.numvia
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
        respuesta += "<br>Datos de contacto: Sin datos de contacto"
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

def login(request):
    if request.method == "POST":
        nombre = request.POST['nombre']
        print(nombre)
        contraseña = request.POST['contra']
        usuario = authenticate(username=nombre, password=contraseña)
        if usuario != None:
            if usuario.is_active:
                auth_login(request, usuario)
    return HttpResponseRedirect('/')

def logout(request):
    #redirigir a /admin/logout
    return redirect('/admin/logout/')

def uploadxml(request):
    #falta poner boton en la pagina principal para cargar los aparcamientos la primera vez
    update()
    return redirect('/')
