from django.db import models
from django.utils import timezone

class Automoviles(models.Model):
    id = models.AutoField(primary_key=True)  # Campo de identificación auto-incremental
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=12, decimal_places=2)  # Hasta 9999999999.99
    cilindraje = models.PositiveIntegerField()
    tipo = models.CharField(max_length=20, blank=True, null=True)  # Ej: Sedán, SUV, etc.
    capacidad_personas = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='automoviles/', blank=True, null=True)  # Campo para la imagen

    def __str__(self):
        return f"{self.marca} {self.modelo}"

class Vendedor(models.Model):
    id_vendedor = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=255)
    correo = models.EmailField(max_length=255)
    antiguedad = models.IntegerField()
    comision = models.DecimalField(max_digits=10, decimal_places=2)

class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    cliente = models.CharField(max_length=255)
    factura_carro = models.IntegerField()  # Asegúrate de definir este campo
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(default=timezone.now)
    precio = models.DecimalField(max_digits=12, decimal_places=2)  # Definir correctamente este campo

class Automovil(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='automoviles/')
    correo_contacto = models.EmailField(max_length=255)  # Correo del contacto

    @property
    def oferta(self):
        return self.precio - 30000  # Calculamos la oferta

    def __str__(self):
        return self.nombre