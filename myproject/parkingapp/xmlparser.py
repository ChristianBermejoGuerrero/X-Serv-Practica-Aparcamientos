from parkingapp.bs4 import BeautifulSoup
from parkingapp.models import Aparcamiento
from parkingapp.models import Distrito
import urllib.request

def update():
    url = "http://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full"
    f = urllib.request.urlopen(url)
    soup = BeautifulSoup(f, 'html.parser')

    print("Uploading XML File. Wait a few seconds please...")
    distrito = Distrito()
    for outside in soup.findAll('contenido'):
        aparc = Aparcamiento()
        for inside in outside.findAll('atributo'):
            if inside.attrs["nombre"] == "NOMBRE":
                aparc.nombre = inside.string
            elif inside.attrs["nombre"] == "CONTENT-URL":
                aparc.link = inside.string
            elif inside.attrs["nombre"] == "NOMBRE-VIA":
                aparc.nombrevia = inside.string
            elif inside.attrs["nombre"] == "CLASE-VIAL":
                aparc.clasevial = inside.string
            elif inside.attrs["nombre"] == "NUM":
                aparc.numvia = inside.string
            elif inside.attrs["nombre"] == "DESCRIPCION": #CDATA
                aparc.descripcion = inside.string
            elif inside.attrs["nombre"] == "BARRIO":
                aparc.barrio = inside.string
            elif inside.attrs["nombre"] == "ACCESIBILIDAD":
                aparc.accesibilidad = int(inside.string)
            elif inside.attrs["nombre"] == "LATITUD":
                aparc.latitud = float(inside.string)
            elif inside.attrs["nombre"] == "LONGITUD":
                aparc.longitud = float(inside.string)
            elif inside.attrs["nombre"] == "DISTRITO":
                try:
                    distritoaux = Distrito.objects.get(nombre=inside.string)
                    aparc.distrito = distritoaux
                except Distrito.DoesNotExist:
                    distritoaux = Distrito.objects.create(nombre=inside.string)
                    aparc.distrito = distritoaux
            elif inside.attrs["nombre"] == "TELEFONO":
                aparc.telefono = inside.string
            elif inside.attrs["nombre"] == "EMAIL":
                aparc.email = inside.string
        aparc.save()
    print("Uploading finished. Thanks for waiting.")
