# En cajero/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Producto, Ventas, VentaProducto

def menu(request):
    return render(request, 'menu.html')


def realizar_venta(request):
    if request.method == 'POST':
        codigo_producto = request.POST.get('codigo_producto', '')
        cantidad = int(request.POST.get('cantidad', 0))
        producto = get_object_or_404(Producto, codigo=codigo_producto)

        subtotal = producto.precio * cantidad

        # Modificación: Convertir el objeto Producto a un diccionario
        producto_info = {
            'nombre': producto.nombre,
            'precio': producto.precio,
            'codigo': producto.codigo,
        }

        # Modificación: Obtener detalles de venta de la sesión
        detalles_venta = request.session.get('detalles_venta', [])
        detalles_venta.append({
            'producto': producto_info,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })
        request.session['detalles_venta'] = detalles_venta

        # Modificación: Calcular el total como la suma de todos los subtotales
        total = sum(detalle['subtotal'] for detalle in detalles_venta)

        # Renderizar la página con los datos actualizados
        return render(request, 'realizar_venta.html', {
            'detalles_venta': detalles_venta,
            'total': total,
        })

    # Modificación: Limpiar la sesión si es una nueva venta
    request.session.pop('detalles_venta', None)
    return render(request, 'realizar_venta.html')

def finalizar_venta(request):
    detalles_venta = request.session.get('detalles_venta', [])
    total = sum(detalle['subtotal'] for detalle in detalles_venta)
    request.session.pop('detalles_venta', None)

    # Guardar la venta en la base de datos
    venta = Ventas.objects.create(total=total)
    for detalle in detalles_venta:
        producto_nombre = detalle['producto']['nombre']
        cantidad = detalle['cantidad']
        VentaProducto.objects.create(venta=venta, producto_nombre=producto_nombre, cantidad=cantidad)

    return render(request, 'boleta.html', {
        'detalles_venta': detalles_venta,
        'total': total,
    })
def guardar_venta(request):
    return redirect('venta')

def generar_boleta(request):
    return render(request, 'boleta.html')

def ventas_totales(request):
    ventas = Ventas.objects.all()
    detalles_ventas = []
    for venta in ventas:
        detalles_venta = VentaProducto.objects.filter(venta=venta)
        detalles_ventas.extend(detalles_venta)

    return render(request, 'ventas_totales.html', {'ventas_detalles': detalles_ventas, 'total_ventas': sum(venta.total for venta in ventas)})

def reiniciar_datos(request):
    Ventas.objects.all().delete()
    VentaProducto.objects.all().delete()
    return redirect('ventas_totales')


