from django.shortcuts import HttpResponse, render, redirect
from web.models import Query, Create, Change, Usuario, Producto, Garage, Categoria, Promocion
from django.core.exceptions import PermissionDenied
from hashlib import sha256
from time import time
from os.path import basename
import code
# Create your views here.

EXTENSIONS = {
    "css":"text/css",
    "js":"text/javascript",
    "jpg":"image/*",
    "jpeg":"image/*",
    "png":"image/*",
    "ico":"image/*",
    }

CHARS = [i for i in range(97,123)]
CHARS += [i for i in range(65,92)]
CHARS += [i for i in range(48,58)]
CHARS += [ord('-'), ord('_'), ord('@'), ord('.')]

def _get_extension(path):
    return path[-path[::-1].index('.'):]

def _curate_email(email):
    z = [0 if ord(char) not in CHARS else 1 for char in email ] 
    if 0 in z:
        return False
    if email.count('@') != 1:
        return False
    return True

def _curate_passwd(pass2, pass1):
    if len(pass2) < 8:
        return 1
    if pass2 != pass1:
        return 2
    return 0

def _eval_photo(request, extension, html):
    if extension not in ["jpg", "jpeg", "png", "gif", 'ico']:
        return render(request, html, {
            'error_photo': "Solo se soportan archivos jpg, png, gif, ico.",
            'isowner': True,
        })
    return True



def _prepare_photo(request):
    photo_name = request.FILES['photo'].__str__()
    extension = _get_extension(photo_name)
    photo_name = sha256((photo_name + str(time())).encode()).hexdigest() + '.' + extension
    return photo_name, extension

def e403():
    raise PermissionDenied()

def render_nologin(request, path="index.html"):
    # TODO: add other forbidden interfaces for non users
    if basename(path) in ["garageList.html", "garageCreate.html", "prodList.html", "prodCreate.html"]:
        e403()
    prods = Producto.objects.all()
    garages = Garage.objects.all()
    promociones = Promocion.objects.filter(expiration_date__gte=time())
    # TODO: productos mas vendidos sql, lista de garajes en inicio?
    return render(request, basename(path), {
        'carrusel': list(promociones),
        'carrusel_len': len(promociones) ,
        'productos': prods,
        'garages': garages,
    })

def handler(request, path=""):
    """
    Main handler
    this handle de majority of request of any files, WITH LOGIC SECURITY
    """
    path = request.META["PATH_INFO"]
    extension = "text/html"
    # URL handling
    if path == "/":
        path = "/Template/index.html"
    if not "Template" in path:
        path = "/Template" + path
    print("PATH: ", path)
    if path[:4] == "/web":
        path = path.replace("/web","")
    # Extension Handling
    e = _get_extension(path)
    if e in EXTENSIONS.keys():
        extension = EXTENSIONS[e]
    # Response
    if "member_id" in request.COOKIES.keys()  and _get_extension(basename(path)) == "html" and not "ñ" in path:
        prods = ""
        garages = ""
        categorias = ""
        promociones = ""
        user = Query(Usuario, session_key = request.COOKIES["member_id"])
        is_owner = False
        glen=""
        if user != None:
            glen = len(Garage.objects.filter(user=user.id))
            is_owner = user.rol
            username = user.nombre
            # TODO: add to this list requirements of all templates T_T
            # TODO: Add others nonrol user interfaces
            if basename(path) in ["garageList.html", "garageCreate.html", "prodList.html", "prodCreate.html"] and not user.rol: 
                e403()
            if basename(path) in ["index.html", "user.html", "prodUser.html"]:
                prods = Producto.objects.all()
            if basename(path) in ["prodList.html"]:
                garages = Query(Garage, user=user.id)
                prods = Producto.objects.filter(garage=Garage.objects.get(user=user.id))
                promociones = Promocion.objects.filter(garage=garages.id)
            if basename(path) in ["garaUser.html" ]:
                garages = Garage.objects.all()
            if basename(path) in ["garageList.html"]: # Pendiente a eliminar
                garages = Garage.objects.filter(user=user.id)
            if basename(path) in ["prodCreate.html"]:
                categorias = Categoria.objects.all()
            if basename(path) in ["index.html", "user.html"]:
                prods = prods.order_by("ventas").reverse()[:8]
            promociones = Promocion.objects.filter(expiration_date__gte=time())
            return render(request, basename(path), {
                'carrusel': list(promociones),
                'carrusel_len': len(promociones) ,
                'username': username,
                'productos': prods,
                'garages': garages,
                'promociones': promociones,
                'categorias': categorias,
                'isowner': is_owner,
                'glen': glen,
            })
        else:
            e403()
    if  _get_extension(basename(path)) == "html" and not "ñ" in path:
        return render_nologin(request, path)
    try:
        return HttpResponse( open("web%s" % path, 'rb').read(), content_type=extension) 
    except:
        # TODO: 404
        return HttpResponse(b"404")

#########################################
    #  Auth
#########################################

def signup(request):
    if request.method != 'POST':
        e403()
    username = request.POST["username"]
    email = request.POST["email"]
    passwd = request.POST["password"]
    passwd1 = request.POST["password1"]

    if not _curate_email(email):
        return auth(request, "sign-up.html", "Este email es incorrecto")
    p = _curate_passwd(passwd, passwd1)
    if p != 0:
        if p == 1:
            return auth(request, "sign-up.html", error_passwd="Password too weak.")
        if p == 2:
            return auth(request, "sign-up.html", error_passwd1="Password does not match.")
    if Query(Usuario, nombre = username) == None:
        if Query(Usuario, email = email) == None and email != "admin@admin.admin":
            # do the auth
            p = sha256(passwd.encode()).hexdigest()
            t = str(int(time()))
            session = sha256((username + t).encode()).hexdigest()[:20]
            Create(Usuario, nombre=username, email=email,password=p, session_key=session)
            html = redirect("/Template/User/user.html")
            html.set_cookie("member_id", value=session, max_age=None)
            return html 
        else:
            return auth(request, "sign-up.html", "Este email ya existe")
    else:
        return auth(request, "sign-up.html","", "Este usuario ya existe")

def signin(request):
    if request.method != "POST":
        e403()
    email = request.POST["email"]
    passwd = request.POST["password"]
    if "ckeckbox" in request.POST.keys():
        max_age = 3600
    else:
        max_age = None
    #Delim Admin
    if email == "admin@admin.admin":
        if passwd == "asdasdasd":
            html = redirect("/root/")
            html.set_cookie("member_id2", value="0", max_age=None)
            return html
    if Query(Usuario, email=email) != None:
        p = sha256(passwd.encode()).hexdigest()
        if Query(Usuario, email=email, password=p) != None:
        #login
            t = str(int(time()))
            session = sha256((email + t).encode()).hexdigest()[:20]
            html = redirect("/Template/User/user.html")
            html.set_cookie("member_id", value=session, max_age=max_age)
            user = Usuario.objects.get(email=email)
            user.session_key=session
            user.save()
            print("SIGNIN:", session)
            return html
        else:
            return auth(request, 'signin.html', error_passwd="Contrasenha incorrecta.")
    else:
        return auth(request, 'signin.html', error_email="Email no existe.")

def auth(request, path, error_email="", error_username="", error_passwd="", error_passwd1=""):
    return render(request, path, {
        "error_email" : error_email,
        'error_username': error_username,
        'error_passwd': error_passwd,
        'error_passwd1': error_passwd1,
    })

def logout(request):
    if not "member_id" in request.COOKIES.keys() and not "member_id2" in request.COOKIES.keys() :
        e403()
    html = redirect("/Template/index.html")
    if "member_id" in request.COOKIES.keys():
        html.delete_cookie("member_id")
    if "member_id2" in request.COOKIES.keys():
        html.delete_cookie("member_id2")
    return html

#######################################################
        # CRUD
#######################################################

def delGarage(request):
    if request.method == "POST":
        if "member_id" in request.COOKIES.keys():
            session_key = request.COOKIES["member_id"]
            username = Query(Usuario, session_key=session_key)
            if username != None:
                Garage.objects.get(user=username.id).delete()
                return redirect("/Template/index.html")
            else:
                e403()
        else:
            e403()
    else:
        e403()

    # user = Query(Usuario,session_key=request.COOKIES["member_id"])
    # if user != None:
    #     Garage.objects.get(user=user.id, id=path).delete()
    #     return redirect('/Template/User/garageList.html')
    # else:
    #     e403()

def deleteProducto(request):
    if request.method == "POST":
        if "member_id" in request.COOKIES.keys():
            session_key = request.COOKIES["member_id"]
            username = Query(Usuario, session_key=session_key)
            if username == None:
                e403()
            garage = Query(Garage, user=username.id)
            id = request.POST["id"]
            Query(Producto,garage=garage.id, id=id).delete()
            return redirect("/Template/prodList.html")
        else:
            e403()
    else:
        e403()


def editProducto(request):
    if request.method == "POST":
        if "member_id" in request.COOKIES.keys():
            session_key = request.COOKIES["member_id"]
            user = Query(Usuario, session_key=session_key)
            if user == None:
                e403()
            nombre = request.POST["nombre"]
            cantidad = request.POST["cantidad"]
            precio = request.POST["precio"]
            descuento = request.POST["descuento"]
            categoria = request.POST["categoria"]
            id = request.POST["id"]
            extesion = ""
            if "photo" in request.FILES.keys():
                photo_name, extension = _prepare_photo(request)
            else:
                photo_name = None
            if precio[0] == "-":
                render(request, "prodEdit.html", {"username": user, "error_precio": "Precio Inválido.", "isowner":True})
            if cantidad[0] == "-" or '.' in cantidad:
                render(request, "prodEdit.html", {"username": user, "error_cantidad": "Cantidad Inválida.", "isowner":True})
            if not float(descuento) >= 0 and not float(descuento) <= 1 :
                render(request, "prodEdit.html", {"username": user, "error_descuento": "Descuento Inválido.", "isowner":True})
            garage = Query(Garage, user=user.id)
            categoria = Query(Categoria, id=int(categoria))
            if photo_name != None:
                value = _eval_photo(request, extension, "prodEdit.html")
                if type(value) == type(bool()):
                    Producto.objects.filter(id=id, garage=garage.id).update(garage=garage, categoria=categoria, nombre=nombre, precio=float(precio), cantidad=int(cantidad), descuento=float(descuento),
                                      photo="/Template/media/" + photo_name)
                    open("web/Template/media/" + photo_name, "bw").write(request.FILES['photo'].read())
                else:
                    return value
            else:
                Producto.objects.filter(id=id, garage=garage.id).update(garage=garage, categoria=categoria, nombre=nombre, precio=float(precio), cantidad=int(cantidad), descuento=float(descuento)),
            return redirect("/Template/prodList.html")
        else:
            e403()
    else:
        e403()

def editProductoView(request):
    if request.method == "POST":
        if "member_id" in request.COOKIES.keys():
            session_key = request.COOKIES["member_id"]
            username = Query(Usuario, session_key=session_key)
            if username == None:
                e403()
            garage = Query(Garage, user=username.id)
            categorias = Categoria.objects.all()
            id = request.POST['id']
            producto = Producto.objects.get(id=id, garage=garage.id)
            return render(request, "prodEdit.html",{
                "username": username,
                "nombre": producto.nombre,
                "descuento": producto.descuento,
                "precio": producto.precio,
                "ventas": producto.ventas,
                "cantidad": producto.cantidad,
                "ventas": producto.ventas,
                "cid": producto.categoria.id,
                "cnombre": producto.categoria.nombre,
                "categorias": categorias,
                "id": id,
                "isowner": True,
            })

        else:
            e403()
    else:
        e403()

def editGarageView(request):
    if request.method == "POST":
        if "member_id" in request.COOKIES.keys():
            session_key = request.COOKIES["member_id"]
            username = Query(Usuario, session_key=session_key)
            if username == None:
                e403()
            id = request.POST['id']
            garage = Query(Garage,id=id, user=username.id)
            glen = len(Garage.objects.filter(user=username.id))
            return render(request, "garageEdit.html",{
                "username": username,
                "id": id,
                "glen": glen,
                "x": garage,
                "isowner": True,
            })
        else:
            e403()
    else:
        e403()

def editGarage(request, path=""):
    if request.method == "POST":
        if "member_id" in request.COOKIES.keys():
            session_key = request.COOKIES["member_id"]
            username = Query(Usuario, session_key=session_key)
            if username == None:
                e403()
            id = request.POST["id"]
            nombre = request.POST["nombre"]
            owner = request.POST["owner"]
            address = request.POST["address"]
            telephone = request.POST["telephone"]
            if "photo" in request.FILES.keys() :
                photo_name, extension = _prepare_photo(request)
            else:
                photo_name = None
            if photo_name != None:
                value = _eval_photo(request, extension, "garageEdit.html")
                if type(value) == type(bool()):
                    Garage.objects.filter(id=id,user=username.id).update(nombre=nombre,owner=owner, address=address,telephone=telephone,
                                      photo="/Template/media/" + photo_name)
                    open("web/Template/media/" + photo_name, "bw").write(request.FILES['photo'].read())
                else:
                    return value
            else:
                Garage.objects.filter(id=id,user=username.id).update(nombre=nombre,owner=owner, address=address,telephone=telephone)
            return redirect("/Template/prodList.html")
        else:
            e403()
    else:
        e403()

def addGarage(request, path=""):
    if request.method == "POST":
        extension = ".jpg"
        if "photo" in request.FILES.keys() :
            photo_name, extension = _prepare_photo(request)
        else:
            photo_name = None
        username = Usuario.objects.get(session_key=request.COOKIES["member_id"])
        if username == None:
            e403()
        nombre = request.POST["nombre"]
        owner = request.POST["owner"]
        address = request.POST["address"]
        telephone = request.POST["telephone"]
        glen = len(Garage.objects.filter(user=username.id))
        if glen != 0:
            e403()
        if Query(Garage, nombre=nombre) != None:
            return render(request, "garageCreate.html", {
                'error_nombre': "El nombre de garaje ya existe",
                    'isowner': True,
                    'glen': 0,
            })
        else:
            if telephone[:3] != "+53" or len(telephone) != 11:
                return render(request, "garageCreate.html", {
                    'error_telephone': "El número de teléfono no es válido.",
                    'isowner': True,
                    'glen': 0,
                })
            if photo_name != None:
                value = _eval_photo(request, extension, "garageCreate.html")
                if type(value) == type(bool()):
                    Garage.objects.create(user=username, nombre=nombre, owner=owner, address=address, telephone=telephone,
                                      photo="/Template/media/" + photo_name)
                    open("web/Template/media/" + photo_name, "bw").write(request.FILES['photo'].read())
                else:
                    return value
            else:
                Garage.objects.create(user=username, nombre=nombre, owner=owner, address=address, telephone=telephone)
            # return sucess
            return redirect("/Template/prodList.html")
    else:
        e403()

def addProducto(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        cantidad = request.POST["cantidad"]
        precio = request.POST["precio"]
        descuento = request.POST["descuento"]
        categoria = request.POST["categoria"]
        extesion = ""
        if "photo" in request.FILES.keys():
            photo_name, extension = _prepare_photo(request)
        else:
            photo_name = None
        if precio[0] == "-":
            render(request, "prodCreate.html", {"error_precio": "Precio Inválido.", "isowner":True})
        if cantidad[0] == "-" or '.' in cantidad:
            render(request, "prodCreate.html", {"error_cantidad": "Cantidad Inválida.", "isowner":True})
        if not float(descuento) >= 0 and not float (descuento) <= 1 :
            render(request, "prodCreate.html", {"error_descuento": "Descuento Inválido.", "isowner":True})
        session = request.COOKIES["member_id"]
        user = Query(Usuario, session_key=session)
        if user == None:
            e403()
        garage = Query(Garage, user=user.id)
        categoria = Query(Categoria, id=int(categoria))
        if photo_name != None:
            value = _eval_photo(request, extension, "prodCreate.html")
            if type(value) == type(bool()):
                Producto.objects.create(garage=garage, categoria=categoria, nombre=nombre, precio=float(precio), cantidad=int(cantidad), descuento=float(descuento),
                                  photo="/Template/media/" + photo_name)
                open("web/Template/media/" + photo_name, "bw").write(request.FILES['photo'].read())
            else:
                return value
        else:
            Producto.objects.create(garage=garage, categoria=categoria, nombre=nombre, precio=float(precio), cantidad=int(cantidad), descuento=float(descuento),
                                  )
        # return sucess
        return redirect("/Template/prodList.html")

    else:
        e403()

def delPromocion(request, path=""):
    if request.method == "POST":
        if 'member_id' in request.COOKIES.keys():
            session_key = request.COOKIES['member_id']
            username = Query(Usuario, session_key=session_key)
            id = request.POST['id']
            if username == None:
                e403()
            garage = Query(Garage, user=username.id)
            Promocion.objects.get(garage=garage.id, id=id).delete()
            return redirect("/Template/prodList.html")
        else:
            e403()
    else:
        e403()



def addPromocion(request, path=""):
    if request.method == "POST":
        if 'member_id' in request.COOKIES.keys():
            session_key = request.COOKIES['member_id']
            username = Query(Usuario, session_key=session_key)
            if username == None:
                e403()
            garage = Query(Garage,user=username.id )
            if "photo" in request.FILES.keys():
                photo_name, extension = _prepare_photo(request)
            else:
                photo_name = None
            if photo_name != None:
                value = _eval_photo(request, extension, "garageCreate.html")
                if type(value) == type(bool()):
                    Promocion.objects.create(garage=garage, expiration_date=int(time() + 3600 * 24 * 30), photo="/Template/media/" + photo_name)
                    open("web/Template/media/" + photo_name, "bw").write(request.FILES['photo'].read())
                else:
                    return value
            else:
                Promocion.objects.create(garage=garage, expiration_date=int(time() + 3600 * 24 * 30))
            return redirect("/Template/prodList.html")
        else:
            e403()
    else:
        e403()

def showProduct(request, id):
    if 'member_id' in request.COOKIES.keys():
        session_key = request.COOKIES["member_id"]
        username = Query(Usuario, session_key=session_key)
        if username != None:
            return render(request, "prodShow.html",{
                'username': username,
                'x': Query(Producto,id=id)
            })
        else:
            e403()
    else:
        return render(request, "prodShow.html",{
            'x': Query(Producto,id=id)
        })

def showGarage(request, id):
    p = Producto.objects.filter(garage=id)
    if 'member_id' in request.COOKIES.keys():
        session_key = request.COOKIES["member_id"]
        username = Query(Usuario, session_key=session_key)
        if username != None:
            return render(request, "garageShow.html",{
                "username": username,
                'x': Query(Garage,id=id),
                'yy': p,
                'len': len(p),
            })
        else:
            e403()
    else:
        return render(request, "garageShow.html",{
            'x': Query(Garage,id=id),
            'yy': p,
            'len': len(p),
        })
    

#####################
 # Search
#####################
def search(request):
    if request.method == "POST":
        string = request.POST['search']
        prods = list(Producto.objects.filter(nombre__contains=string))
        garages = Garage.objects.filter(nombre__contains=string)
        categorias = list(Categoria.objects.all())
        prods.extend(garages)
        prods.sort(key=lambda x: x.nombre)
        categorias_name = [ i.nombre.lower() for i in categorias]
        if string.lower() in categorias_name:
            categoria = Categoria.objects.get(nombre__contains=string.lower())
            try:
                p = list(Producto.objects.filter(categoria=categoria.id))
                p.extend(prods)
                prods = p
            except:
                pass
        if "member_id" in request.COOKIES.keys():
            session_key = request.COOKIES["member_id"]
            username = Query(Usuario, session_key=session_key)
            if username == None:
                e403()
            return render(request, "search.html",{
                'username': username,
                'x': prods,
            })
        return render(request, "search.html",{
            'x': prods,
        })

    else:
        e403()


# def media(request, path):
#     path = request.META["PATH_INFO"]
#     print(path)
#     if path == "/":
#         path = "/Template/index.html"
#     if not "Template" in path:
#         path = "/Template" + path
#     return HttpResponse( open("web%s" % path, "rb").read(), content_type="image/*") 
#
# # def media(request, path):
#     # return HttpResponse( open("web/Template/media/%s" % path, "rb").read(), content_type="image/*")
#
# def script(request, path):
#     return HttpResponse( open("web/Template/scripts/%s" % path, "r").read(), content_type="text/javascript")
#
# def icons(request, path):
#     return HttpResponse( open("web/Template/media/icons/%s" % path, "rb").read(), content_type="image/*")
#
# def css(request, path):
#     return HttpResponse( open("web/Template/css/%s" % path, "r").read(), content_type="text/css")
    # while True:
        # print(eval(input("\n$> ")))

# def deleteGarage(request,path):
#     # Todo: POST method
#     user = Query(Usuario,session_key=request.COOKIES["member_id"])
#     if user != None:
#         Garage.objects.get(user=user.id, id=path).delete()
#         return redirect('/Template/User/garageList.html')
#     else:
#         e403()
