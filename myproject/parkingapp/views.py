from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from parkingapp.xmlparser import update
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context, RequestContext, Template
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from parkingapp.models import Aparcamiento, PaginaUsuario, AparcSelect, Distrito, Comentario, Estilo

globAcc = False
start = 0
end = 5

@csrf_exempt
def showPrincipal(request):
    global globAcc
    mostrar = False
    mostrarbutton = True
    template = get_template('button.html')
    userlist = User.objects.all()
    pageuserlist = PaginaUsuario.objects.all()
    if len(userlist) != len(pageuserlist):
        for user in userlist:
            paginausuario = PaginaUsuario(usuario=user,titulo=("Pagina de " + user.username))
            paginausuario.save()
    pageuserlist = PaginaUsuario.objects.all()
    aparclist = Aparcamiento.objects.all()
    if len(aparclist) != 0:
        mostrarbutton = False
    aparclistOrden = aparclist.exclude(numcomments=0).order_by('numcomments').reverse()[:5]
    aparclistAcc = Aparcamiento.objects.all().filter(accesibilidad=1)
    aparclistAccOrden = aparclistAcc.exclude(numcomments=0).order_by('numcomments').reverse()[:5]
    if len(aparclistAccOrden) != 0:
        mostrar = True
    elif len(aparclistOrden) != 0:
        mostrar = True
    if request.method == "POST" and globAcc == False:
        globAcc = True
    elif request.method == "POST" and globAcc == True:
        globAcc = False
    if request.user.is_authenticated():
        try:
            estilocss = Estilo.objects.get(usuario=request.user)
            c = RequestContext(request, {'globAcc':globAcc,
                                         'mostrar':mostrar,
                                         'mostrarbutton':mostrarbutton,
                                         'estilo':estilocss,
                                         'pageuserlist':pageuserlist,
                                         'aparclistOrden':aparclistOrden,
                                         'aparclistAccOrden':aparclistAccOrden})
        except Estilo.DoesNotExist:
            c = RequestContext(request, {'globAcc':globAcc,
                                         'mostrar':mostrar,
                                         'mostrarbutton':mostrarbutton,
                                         'pageuserlist':pageuserlist,
                                         'aparclistOrden':aparclistOrden,
                                         'aparclistAccOrden':aparclistAccOrden})
    else:
        c = RequestContext(request, {'globAcc':globAcc,
                                     'mostrar':mostrar,
                                     'mostrarbutton':mostrarbutton,
                                     'pageuserlist':pageuserlist,
                                     'aparclistOrden':aparclistOrden,
                                     'aparclistAccOrden':aparclistAccOrden})
    return HttpResponse(template.render(c))

@csrf_exempt
def showUserpage(request,nombre):
    global start,end
    try:
        mostrar = False
        mostrarbutton = False
        template = get_template('userpage.html')
        useraux = User.objects.get(username=nombre)
        pageuser = PaginaUsuario.objects.get(usuario=useraux)
        aparclistSelect = AparcSelect.objects.all().filter(pagUsuario=pageuser)
        aparclistAccSelect = []
        print(len(aparclistSelect))
        if len(aparclistSelect) != 0:
            for aparcSelect in aparclistSelect:
                if aparcSelect.aparcamiento.accesibilidad == 1:
                    aparclistAccSelect.append(aparcSelect)
        if request.method == "POST" and "tamano" in request.POST and "color" in request.POST:
            nuevocolor = request.POST['color']
            nuevotamano = request.POST['tamano']
            useraux = User.objects.get(username=request.user.username)
            try:
                Estilo.objects.get(usuario=useraux)
                estilocss = Estilo.objects.get(usuario=request.user)
                estilocss.tamano = nuevotamano
                estilocss.color = nuevocolor
                estilocss.save()
            except Estilo.DoesNotExist:
                estilo = Estilo(usuario=useraux,tamano=nuevotamano,color=nuevocolor)
                estilo.save()
            return HttpResponseRedirect("/" + nombre)
        elif request.method == "POST" and "nuevotitulo" in request.POST:
            nuevotitulo = request.POST['nuevotitulo']
            useraux = User.objects.get(username=request.user.username)
            pageuser = PaginaUsuario.objects.get(usuario=useraux)
            pageuser.titulo = nuevotitulo
            pageuser.save()
            return HttpResponseRedirect("/" + nombre)
        elif request.method == "POST":
            start = start + 5
            end = end + 5
        elif request.method == "GET":
            start = 0
            end = 5
            if len(aparclistSelect) > int(end) and  globAcc == False:
                mostrarbutton = True
            elif len(aparclistAccSelect) > int(end) and globAcc == True:
                mostrarbutton = True
        if len(aparclistAccSelect) != 0 and globAcc == True:
            mostrar = True
        elif len(aparclistSelect) != 0 and globAcc == False:
            mostrar = True
        if request.user.is_authenticated():
            try:
                estilocss = Estilo.objects.get(usuario=request.user)
                c = RequestContext(request, {'globAcc':globAcc,
                                             'mostrarbutton':mostrarbutton,
                                             'mostrar':mostrar,
                                             'estilo':estilocss,
                                             'paginausuario':pageuser,
                                             'aparclistSelect':aparclistSelect[start:end],
                                             'aparclistAccSelect':aparclistAccSelect[start:end]})
            except Estilo.DoesNotExist:
                c = RequestContext(request, {'globAcc':globAcc,
                                             'mostrarbutton':mostrarbutton,
                                             'mostrar':mostrar,
                                             'paginausuario':pageuser,
                                             'aparclistSelect':aparclistSelect[start:end],
                                             'aparclistAccSelect':aparclistAccSelect[start:end]})
        else:
            c = RequestContext(request, {'globAcc':globAcc,
                                         'mostrarbutton':mostrarbutton,
                                         'mostrar':mostrar,
                                         'paginausuario':pageuser,
                                         'aparclistSelect':aparclistSelect[start:end],
                                         'aparclistAccSelect':aparclistAccSelect[start:end]})
    except (User.DoesNotExist,PaginaUsuario.DoesNotExist):
        template = get_template('error.html')
        c = RequestContext(request,{})
    return HttpResponse(template.render(c))

@csrf_exempt
def showAllParkings(request):
    try:
        mostrar = False
        template = get_template('allAparcs.html')
        aparclist = Aparcamiento.objects.all()
        aparclistAcc = aparclist.filter(accesibilidad=1)
        distritolist = Distrito.objects.all()
        if len(aparclistAcc) != 0 and globAcc == True:
            mostrar = True
        elif len(aparclist) != 0 and globAcc == False:
            mostrar = True
        if request.method == "GET":
            if request.user.is_authenticated():
                try:
                    estilocss = Estilo.objects.get(usuario=request.user)
                    c = RequestContext(request, {'globAcc':globAcc,
                                                 'mostrar':mostrar,
                                                 'estilo':estilocss,
                                                 'aparclist':aparclist,
                                                 'distritolist':distritolist,
                                                 'aparclistAcc':aparclistAcc})
                except Estilo.DoesNotExist:
                    c = RequestContext(request, {'globAcc':globAcc,
                                                 'mostrar':mostrar,
                                                 'aparclist':aparclist,
                                                 'distritolist':distritolist,
                                                 'aparclistAcc':aparclistAcc})
            else:
                c = RequestContext(request, {'globAcc':globAcc,
                                             'mostrar':mostrar,
                                             'aparclist':aparclist,
                                             'distritolist':distritolist,
                                             'aparclistAcc':aparclistAcc})
    except (User.DoesNotExist,PaginaUsuario.DoesNotExist):
        template = get_template('error.html')
        c = RequestContext(request,{})

    return HttpResponse(template.render(c))


@csrf_exempt
def showOneParking(request,identificador):
    try:
        template = get_template('oneAparc.html')
        aparcaux = Aparcamiento.objects.get(id=identificador)
        commentlist = Comentario.objects.all().filter(aparcamiento=aparcaux)
        if request.method == "POST" and "newcomment" in request.POST:
            comment = request.POST['newcomment']
            nuevocomentario = Comentario(text=comment,aparcamiento=aparcaux)
            nuevocomentario.save()
            if aparcaux.numcomments == None:
                aparcaux.numcomments = 1
            else:
                aparcaux.numcomments = aparcaux.numcomments + 1
            aparcaux.save()
            return HttpResponseRedirect("/aparcamientos/" + identificador)
        elif request.method == "POST":
            pageuser = PaginaUsuario.objects.get(usuario=request.user)
            try:
                select = AparcSelect.objects.get(aparcamiento=aparcaux)
            except AparcSelect.DoesNotExist:
                select = AparcSelect(usuario=request.user,pagUsuario=pageuser,aparcamiento=aparcaux)
                select.save()
            return HttpResponseRedirect("/aparcamientos/" + identificador)

        if request.user.is_authenticated():
            try:
                estilocss = Estilo.objects.get(usuario=request.user)
                c = RequestContext(request, {'aparc':aparcaux,
                                             'estilo':estilocss,
                                             'commentlist':commentlist})
            except Estilo.DoesNotExist:
                c = RequestContext(request, {'aparc':aparcaux,
                                             'commentlist':commentlist})
        else:
            c = RequestContext(request, {'aparc':aparcaux,
                                         'commentlist':commentlist})
    except (User.DoesNotExist,PaginaUsuario.DoesNotExist,Aparcamiento.DoesNotExist):
        template = get_template('error.html')
        c = RequestContext(request,{})

    return HttpResponse(template.render(c))

@csrf_exempt
def filtdistrito(request,nombredistr):
    try:
        template = get_template('allAparcs.html')
        aparclist = Aparcamiento.objects.all()
        aparclistAcc = aparclist.filter(accesibilidad=1)
        distritolist = Distrito.objects.all()
        distritoaux = Distrito.objects.get(nombre=nombredistr)
        aparclistFilt = aparclist.filter(distrito=distritoaux)
        aparclistAccFilt = aparclistFilt.filter(accesibilidad=1)
        if request.user.is_authenticated():
            try:
                estilocss = Estilo.objects.get(usuario=request.user)
                c = RequestContext(request, {'globAcc':globAcc,
                                             'estilo':estilocss,
                                             'aparclist':aparclistFilt,
                                             'distritolist':distritolist,
                                             'aparclistAcc':aparclistAccFilt})
            except Estilo.DoesNotExist:
                c = RequestContext(request, {'globAcc':globAcc,
                                             'aparclist':aparclistFilt,
                                             'distritolist':distritolist,
                                             'aparclistAcc':aparclistAccFilt})
        else:
            c = RequestContext(request, {'globAcc':globAcc,
                                         'aparclist':aparclistFilt,
                                         'distritolist':distritolist,
                                         'aparclistAcc':aparclistAccFilt})
    except (User.DoesNotExist,PaginaUsuario.DoesNotExist,Distrito.DoesNotExist):
        template = get_template('error.html')
        c = RequestContext(request,{})

    return HttpResponse(template.render(c))

def userxml(request,nombre):
    template = get_template('xmluser.html')
    useraux = User.objects.get(username=nombre)
    pageuser = PaginaUsuario.objects.get(usuario=useraux)
    aparclistSelect = AparcSelect.objects.all().filter(pagUsuario=pageuser)
    c = RequestContext(request, {'aparclistSelect':aparclistSelect})
    return HttpResponse(template.render(c), content_type="text/xml")

def about(request):
    template = get_template('about.html')
    if request.user.is_authenticated():
        try:
            nuevoestilo = Estilo.objects.get(usuario=request.user)
            c = RequestContext(request, {'estilo':nuevoestilo})
        except Estilo.DoesNotExist:
            c = RequestContext(request, {})
    else:
        c = RequestContext(request, {})

    return HttpResponse(template.render(c))

def login(request):
    if request.method == "POST":
        nombre = request.POST['nombre']
        contrasena = request.POST['contra']
        usuario = authenticate(username=nombre, password=contrasena)
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
