#cajero/models.py
from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    codigo = models.CharField(max_length=5, unique=True)  # Longitud de código ajustada

    def obtener_precio(self):
        return self.precio

class Ventas(models.Model):
    total = models.IntegerField()
    # Otros campos necesarios para tu modelo Ventas

    def __str__(self):
        return f'Total: {self.total}'
    
class VentaProducto(models.Model):
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    producto_nombre = models.CharField(max_length=50)
    cantidad = models.IntegerField()

    def __str__(self):
        return f'{self.producto_nombre} - {self.cantidad}'
