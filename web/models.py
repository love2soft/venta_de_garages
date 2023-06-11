from django.db import models

# Create your models here.

def Query(object, **kword):
    try:
        return object.objects.get(**kword)
    except:
        return None

def Create(object, **kword):
    object.objects.create(**kword)

def Change(object,key, value, **kword):
    o = object.objects.get(**kword)
    o[key] = value

class Categoria(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=65)
    rol = models.BooleanField(default=True)
    session_key = models.CharField(max_length=20,default="null")
    def __str__(self):
        return self.nombre + " | " + self.email

class Garage(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    owner = models.CharField(max_length=40)
    telephone = models.CharField(max_length=11)
    photo = models.ImageField(upload_to="web/Template/media/", default="/Template/media/noimage.png")
    def __str__(self):
        return self.nombre + " | " + self.user.nombre

class Producto(models.Model):
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
    precio = models.FloatField()
    ventas = models.IntegerField(default=0)
    cantidad = models.IntegerField()
    descuento = models.FloatField(default=1)
    photo = models.ImageField(upload_to="web/Template/media/", default="/Template/media/noimage.png")
    def __str__(self):
        return self.nombre + " | " + self.garage.nombre

class Promocion(models.Model):
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="web/Template/media/", default="/Template/media/noimage.png")
    expiration_date = models.PositiveIntegerField()
    def __str__(self):
        return self.garage.nombre + " | " + str(self.photo)


