from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *
from django.db.models import Count
import random
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def dashboard_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige al usuario a la página de inicio
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request,'login.html')


def dashboard_home(request):
    return render(request, 'home.html')

def dashboard_automoviles(request):
    autos_por_marca = Automoviles.objects.values('marca').annotate(total=Count('id')).order_by('marca')
    marca_grupos = {}
    
    for marca in autos_por_marca:
        marca_nombre = marca['marca']
        marca_grupos[marca_nombre] = Automoviles.objects.filter(marca=marca_nombre).order_by('modelo')[:10]
    
    return render(request, 'template_automoviles.html', {'marca_grupos': marca_grupos})


def dashboard_diagramas(request):
    automoviles = Automoviles.objects.all()
    
    # Crear un diccionario para almacenar los datos agrupados por tipo
    datos_por_tipo = {}
    
    for auto in automoviles:
        tipo = auto.tipo or 'Sin Tipo'  # Maneja el caso donde tipo sea None
        if tipo not in datos_por_tipo:
            datos_por_tipo[tipo] = {'modelos': [], 'precios': []}
        datos_por_tipo[tipo]['modelos'].append(auto.modelo)
        datos_por_tipo[tipo]['precios'].append(float(auto.precio))
    
    # Preparar datos para la plantilla
    context = {
        'datos_por_tipo': datos_por_tipo,
    }
    
    return render(request, 'template_diagramas.html', context)

def dashboard_vendedores(request):
    vendedores = Vendedor.objects.all()
    return render(request,'template_vendedores.html', {'vendedores': vendedores})

def dashboard_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'template_facturas.html', {'facturas': facturas})

def calcular_regresion_lineal(x, y):
    n = len(x)
    suma_x = sum(x)
    suma_y = sum(y)
    suma_xy = sum(x[i] * y[i] for i in range(n))
    suma_xx = sum(xi ** 2 for xi in x)

    m = (n * suma_xy - suma_x * suma_y) / (n * suma_xx - suma_x ** 2)
    b = (suma_y - m * suma_x) / n
    return m, b

def calcular_regresion_cuadratica(x, y):
    n = len(x)
    suma_x = sum(x)
    suma_y = sum(y)
    suma_xx = sum(xi ** 2 for xi in x)
    suma_xy = sum(x[i] * y[i] for i in range(n))
    suma_xxx = sum(xi ** 3 for xi in x)
    suma_xxxx = sum(xi ** 4 for xi in x)
    suma_xxy = sum(x[i] ** 2 * y[i] for i in range(n))

    denominador = (n * suma_xx * suma_xxxx + 2 * suma_x * suma_xxx * suma_xx - suma_x ** 2 * suma_xxxx - n * suma_xxx ** 2 - suma_xx ** 2 * suma_x)

    a = (n * suma_xx * suma_xxy + suma_x * suma_xy * suma_xxx - suma_y * suma_xxx ** 2 - suma_xx * suma_x * suma_xxy) / denominador
    b = (n * suma_xxy * suma_xx - suma_y * suma_xx ** 2 - suma_x * suma_xx * suma_xy) / denominador
    c = (suma_y - b * suma_x - a * suma_xx) / n

    return a, b, c

def algoritmo_kalman(precios):
    # Inicializar parámetros del filtro de Kalman
    n = len(precios)
    x_hat = [0] * n  # Estimaciones
    P = [0] * n  # Covarianza
    Q = 1e-5  # Ruido del proceso
    R = 0.1  # Ruido de la medición

    # Inicialización
    x_hat[0] = precios[0]
    P[0] = 1.0

    for k in range(1, n):
        # Predicción
        x_hat[k] = x_hat[k-1]
        P[k] = P[k-1] + Q

        # Medición
        y = precios[k]

        # Actualización
        K = P[k] / (P[k] + R)  # Ganancia de Kalman
        x_hat[k] += K * (y - x_hat[k])
        P[k] = (1 - K) * P[k]

    return x_hat

def dashboard_predictivo(request):
    # Obtener todos los automóviles
    automoviles = Automoviles.objects.all()
    
    # Extraer precios en una lista
    precios = [float(auto.precio) for auto in automoviles]
    x = list(range(len(precios)))

    # Calcular regresiones
    m, b = calcular_regresion_lineal(x, precios)
    coef_cuadratica = calcular_regresion_cuadratica(x, precios)
    precios_kalman = algoritmo_kalman(precios)

    # Preparar datos para la plantilla
    context = {
        'precios': precios,
        'x': x,
        'm': m,
        'b': b,
        'coef_cuadratica': coef_cuadratica,
        'precios_kalman': precios_kalman,
    }
    
    return render(request, 'template_predictivo.html', context)

def dashboard_oportunidades(request):
    # Tomamos todos los autos de la base de datos
    autos = list(Automovil.objects.all())
    
    # Verificamos cuántos autos hay
    num_autos = len(autos)
    
    if num_autos == 0:
        # Manejar el caso de no tener autos
        return render(request, 'ofertas.html', {'autos': [], 'mensaje': 'No hay autos disponibles en este momento.'})

    # Si hay menos de 3 autos, ajustamos la cantidad de autos a seleccionar
    cantidad_a_seleccionar = min(num_autos, 3)
    
    # Seleccionamos los autos aleatorios
    autos_aleatorios = random.sample(autos, cantidad_a_seleccionar)

    # Creamos una lista para almacenar autos y sus ofertas
    autos_con_oferta = []
    
    # Calculamos la oferta (precio - 30,000) y agregamos al objeto
    for auto in autos_aleatorios:
        oferta = auto.precio - 30000  # Calculamos la oferta
        autos_con_oferta.append({
            'nombre': auto.nombre,
            'precio': auto.precio,
            'descripcion': auto.descripcion,
            'imagen': auto.imagen.url,
            'oferta': oferta,
            'id': auto.id
        })

    # Si el usuario envía una oferta
    if request.method == "POST":
        auto_id = request.POST.get('auto_id')
        auto = Automovil.objects.get(id=auto_id)
        # Lista de correos electrónicos a los que se enviará la oferta
        destinatarios = [
        ]
        enviar_oferta_por_correo(auto, destinatarios)
        return redirect('mensaje_exitoso') 
    # Renderizamos el template
    return render(request, 'template_oportunidades.html', {'autos': autos_con_oferta})

def enviar_oferta_por_correo(auto, destinatarios):
    # Crear el cuerpo del correo con la oferta
    mensaje = f"Hola,\n\nTienes una nueva oferta para el automóvil:\n\n" \
              f"Nombre: {auto.nombre}\n" \
              f"Precio: ${auto.precio}\n" \
              f"Oferta: ${auto.oferta}\n" \
              f"Descripción: {auto.descripcion}\n\n" \
              f"¡Gracias por tu interés!"

    # Enviar el correo a la lista de destinatarios
    send_mail(
        subject='Nueva Oferta de Automóvil',
        message=mensaje,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=destinatarios,
        fail_silently=False,
    )

def dashboard_comparador(request):
    autos = Automoviles.objects.all()  # Obtener todos los autos disponibles
    selected_autos = []

    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_autos')  # Obtener los IDs de los autos seleccionados
        # Filtrar los IDs vacíos
        selected_ids = [id for id in selected_ids if id]  
        selected_autos = Automoviles.objects.filter(id__in=selected_ids)  # Filtrar los autos seleccionados
        

    return render(request, 'template_comparador.html', {'autos': autos, 'selected_autos': selected_autos})

def dashboard_desiciones(request):
    return render(request, 'template_desiciones.html')

def mensaje_exitoso_view(request):
    return render(request,'mensaje_exitoso.html')