from django.shortcuts import render, HttpResponse
from django.core.exceptions import PermissionDenied
from django.utils.autoreload import raise_last_exception
from web.models import Usuario, Garage, Producto, Promocion, Categoria
# Create your views here.

def e403():
    raise PermissionDenied()


def main(request, path=""):
    if "member_id2" not in request.COOKIES.keys():
        e403()
    if request.method == "POST":
        if "ccategoria" in path:
            nombre = request.POST["nombre"]
            Categoria.objects.create(nombre=nombre)
            html = render(request, "acategoria.html",{"xs":Categoria.objects.all()})
        return html
    if path == "":
        html = render(request, "amain.html",{"xs":Usuario.objects.all()})
    if path == "agarage.html":
        html = render(request, "agarage.html",{"xs":Garage.objects.all()})
    if path == "aproducto.html":
        html = render(request, "aproducto.html",{"xs":Producto.objects.all()})
    if path == "apromocion.html":
        html = render(request, "apromocion.html",{"xs":Promocion.objects.all()})
    if path == "acategoria.html":
        html = render(request, "acategoria.html",{"xs":Categoria.objects.all()})
    if "duser" in path:
        path = path.replace("duser", "")
        Usuario.objects.get(id=int(path)).delete()
        html = render(request, "amain.html",{"xs":Usuario.objects.all()})
    if "dgarage" in path:
        path = path.replace("dgarage", "")
        Garage.objects.get(id=int(path)).delete()
        html = render(request, "agarage.html",{"xs":Garage.objects.all()})
    if "dproducto" in path:
        path = path.replace("dproducto", "")
        Producto.objects.get(id=int(path)).delete()
        html = render(request, "aproducto.html",{"xs":Producto.objects.all()})
    if "dpromocion" in path:
        path = path.replace("dpromocion", "")
        Promocion.objects.get(id=int(path)).delete()
        html = render(request, "apromocion.html",{"xs":Promocion.objects.all()})
    if "dcategoria" in path:
        path = path.replace("dcategoria", "")
        Categoria.objects.get(id=int(path)).delete()
        html = render(request, "acategoria.html",{"xs":Categoria.objects.all()})
    return html

