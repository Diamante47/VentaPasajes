from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Bus, Conductor, Ruta, Horario, Cliente, Pasaje, Factura
from django.utils.timezone import now
from django.db.models import Sum
import csv
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from datetime import datetime, timedelta

# Create your views here.
def inicio(request):
    return render(request, 'nuevoCliente.html')

@login_required  # Solo permite el acceso a usuarios autenticados
def administrador(request):
    return render(request, 'administrador.html')


        #BUSES
def nuevoBus(request):
    return render(request, 'nuevoBus.html')  # Ajustado para tu estructura


def listadoBuses(request):
    buses = Bus.objects.all()  # Recupera los datos de los buses
    return render(request, 'listadoBuses.html', {'buses': buses})

def guardarBus(request):
    if request.method == 'POST':
        placa = request.POST.get('txt_placa')
        modelo = request.POST.get('txt_modelo')
        capacidad = request.POST.get('txt_capacidad')

        # Verifica si ya existe un bus con la misma placa
        if Bus.objects.filter(placa=placa).exists():
            messages.error(request, "Ya existe un bus con la placa proporcionada.")
            return redirect('nuevoBus')  # Redirige al formulario para intentar nuevamente

        # Si no existe, crea el nuevo bus
        Bus.objects.create(placa=placa, modelo=modelo, capacidad=capacidad)
        messages.success(request, "Bus guardado exitosamente.")
        return redirect('listadoBuses')  # Redirige al listado de buses
    else:
        return redirect('nuevoBus')
    
def eliminarBus(request,id):
    busEliminar=Bus.objects.get(id=id)
    busEliminar.delete()
    messages.success(request,"Bus eliminado Exitosamente")
    return redirect('/listadoBuses')

def editarBus(request, id):
    try:
        busEditar = Bus.objects.get(id=id)
        return render(request, "editarBus.html", {'bus': busEditar})
    except Bus.DoesNotExist:
        messages.error(request, "El bus especificado no existe.")
        return redirect('listadoBuses')

def procesarEdicionBus(request):
    if request.method == 'POST':
        bus_id = request.POST.get('id')
        try:
            # Busca el bus con el ID proporcionado
            bus = Bus.objects.get(id=bus_id)
        except Bus.DoesNotExist:
            messages.error(request, "El bus especificado no existe.")
            return redirect('listadoBuses')

        # Recupera los valores enviados desde el formulario
        placa = request.POST.get('txt_placa')
        modelo = request.POST.get('txt_modelo')
        capacidad = request.POST.get('txt_capacidad')

        # Verifica que los campos no estén vacíos
        if not placa or not modelo or not capacidad:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('editar_bus', id=bus_id)

        # Actualiza los valores del bus
        bus.placa = placa
        bus.modelo = modelo
        bus.capacidad = capacidad
        bus.save()

        # Mensaje de éxito
        messages.success(request, "Bus actualizado exitosamente.")
        return redirect('listadoBuses')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('listadoBuses')
    

        #Conductores

def nuevoConductor(request):
    buses = Bus.objects.all()
    return render(request, 'nuevoConductor.html', {'buses': buses})

def listadoConductores(request):
    conductores = Conductor.objects.all()  # Recupera los datos de los buses
    return render(request, 'listadoConductores.html', {'conductores': conductores})

def guardarConductor(request):
    if request.method == 'POST':
        nombre = request.POST.get('txt_nombre')
        apellido = request.POST.get('txt_apellido')
        dni = request.POST.get('txt_dni')
        telefono = request.POST.get('txt_telefono')
        email = request.POST.get('txt_email')
        bus_id = request.POST.get('bus')

        # Verifica si ya existe un conductor con el mismo DNI
        if Conductor.objects.filter(dni=dni).exists():
            messages.error(request, "Ya existe un conductor con el DNI proporcionado.")
            return redirect('nuevoConductor')

        # Verifica si ya existe un conductor asignado al mismo bus
        if Conductor.objects.filter(bus_id=bus_id).exists():
            messages.error(request, "El bus seleccionado ya tiene un conductor asignado.")
            return redirect('nuevoConductor')
        
        # Verifica si ya existe un conductor con el mismo email
        if Conductor.objects.filter(email=email).exists():
            messages.error(request, "el correo seleccionado ya esta registrado con otro conductor")
            return redirect('nuevoConductor')

        # Guarda el nuevo conductor
        bus = Bus.objects.get(id=bus_id)
        Conductor.objects.create(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            telefono=telefono,
            email=email,
            bus=bus
        )
        messages.success(request, "Conductor guardado exitosamente.")
        return redirect('listadoConductores')
    else:
        return redirect('nuevoConductor')

def eliminarConductor(request,id):
    conductorEliminar=Conductor.objects.get(id=id)
    conductorEliminar.delete()
    messages.success(request,"Conductor eliminado Exitosamente")
    return redirect('/listadoConductores')

def editarConductor(request, id):
    try:
        conductorEditar = Conductor.objects.select_related('bus').get(id=id)
        busesDisponibles = Bus.objects.all()  # Lista de buses disponibles para asignar
        return render(request, "editarConductor.html", {
            'conductor': conductorEditar,
            'buses': busesDisponibles
        })
    except Conductor.DoesNotExist:
        messages.error(request, "El conductor especificado no existe.")
        return redirect('listadoConductores')

def procesarEdicionConductor(request):
    if request.method == 'POST':
        conductor_id = request.POST.get('id')
        try:
            # Busca el conductor con el ID proporcionado
            conductor = Conductor.objects.get(id=conductor_id)
        except Conductor.DoesNotExist:
            messages.error(request, "El conductor especificado no existe.")
            return redirect('listadoConductores')

        # Recupera los valores enviados desde el formulario
        nombre = request.POST.get('txt_nombre')
        apellido = request.POST.get('txt_apellido')
        dni = request.POST.get('txt_dni')
        telefono = request.POST.get('txt_telefono')
        email = request.POST.get('txt_email')
        bus_id = request.POST.get('bus_id')

        # Verifica que los campos no estén vacíos
        if not nombre or not apellido or not dni or not telefono or not email or not bus_id:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('editar_conductor', id=conductor_id)

        # Verifica que el DNI y el email sean únicos si se actualizan
        if Conductor.objects.exclude(id=conductor_id).filter(dni=dni).exists():
            messages.error(request, "El DNI ya está registrado.")
            return redirect('editar_conductor', id=conductor_id)
        if Conductor.objects.exclude(id=conductor_id).filter(email=email).exists():
            messages.error(request, "El email ya está registrado.")
            return redirect('editar_conductor', id=conductor_id)

        # Actualiza los valores del conductor
        conductor.nombre = nombre
        conductor.apellido = apellido
        conductor.dni = dni
        conductor.telefono = telefono
        conductor.email = email
        conductor.bus_id = bus_id
        conductor.save()

        # Mensaje de éxito
        messages.success(request, "Conductor actualizado exitosamente.")
        return redirect('listadoConductores')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('listadoConductores')

        #Rutas

def nuevaRuta(request):
    return render(request, 'nuevaRuta.html')  # Ajustado para tu estructura


def listadoRutas(request):
    rutas = Ruta.objects.all()  # Recupera los datos de los buses
    return render(request, 'listadoRutas.html', {'rutas': rutas})

def guardarRuta(request):
    if request.method == 'POST':
        origen = request.POST.get('txt_origen')
        destino = request.POST.get('txt_destino')

        try:
            # Crea la nueva ruta
            Ruta.objects.create(
                origen=origen,
                destino=destino
            )

            messages.success(request, "Ruta guardada exitosamente.")
            return redirect('listadoRutas')
        except Exception as e:
            messages.error(request, f"Hubo un error al guardar la ruta: {str(e)}")
            return redirect('nuevaRuta')

    return redirect('nuevaRuta')
    
def eliminarRuta(request,id):
    rutaEliminar=Ruta.objects.get(id=id)
    rutaEliminar.delete()
    messages.success(request,"Ruta eliminada Exitosamente")
    return redirect('/listadoRutas')

def editarRuta(request, id):
    try:
        # Busca la ruta con el ID proporcionado
        rutaEditar = Ruta.objects.get(id=id)
        return render(request, "editarRuta.html", {'ruta': rutaEditar})
    except Ruta.DoesNotExist:
        # Si la ruta no existe, muestra un mensaje de error y redirige al listado
        messages.error(request, "La ruta especificada no existe.")
        return redirect('listadoRutas')


def procesarEdicionRuta(request):
    if request.method == 'POST':
        ruta_id = request.POST.get('id')
        try:
            ruta = Ruta.objects.get(id=ruta_id)
        except Ruta.DoesNotExist:
            messages.error(request, "La ruta especificada no existe.")
            return redirect('listadoRutas')

        # Actualiza los datos de la ruta
        origen = request.POST.get('txt_origen')
        destino = request.POST.get('txt_destino')

        if not origen or not destino:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('editar_ruta', id=ruta_id)

        ruta.origen = origen
        ruta.destino = destino
        ruta.save()

        messages.success(request, "Ruta actualizada exitosamente.")
        return redirect('listadoRutas')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('listadoRutas')
    
        #Horarios
    
def nuevoHorario(request):
    # Obtenemos todos los buses y rutas disponibles
    buses = Bus.objects.all()
    rutas = Ruta.objects.all()
    return render(request, 'nuevoHorario.html', {'buses': buses, 'rutas': rutas})

def listadoHorarios(request):
    horarios = Horario.objects.all()  # Recupera los datos de los buses
    return render(request, 'listadoHorarios.html', {'horarios': horarios})

def guardarHorario(request):
    if request.method == 'POST':
        ruta_id = request.POST.get('ruta')  # ID de la ruta seleccionada
        bus_id = request.POST.get('bus')  # ID del bus seleccionado
        fecha = request.POST.get('txt_fecha')  # Fecha del horario
        hora_partida = request.POST.get('txt_hora_partida')  # Hora de salida
        hora_llegada = request.POST.get('txt_hora_llegada')  # Hora de llegada
        costo_pasaje = request.POST.get('txt_costo_pasaje')  # Costo del pasaje

        # Validaciones de existencia
        try:
            ruta = Ruta.objects.get(id=ruta_id)
        except Ruta.DoesNotExist:
            messages.error(request, "La ruta seleccionada no existe.")
            return redirect('nuevoHorario')

        try:
            bus = Bus.objects.get(id=bus_id)
        except Bus.DoesNotExist:
            messages.error(request, "El bus seleccionado no existe.")
            return redirect('nuevoHorario')

        # Verifica si ya existe un horario con el mismo bus, fecha y hora de partida
        if Horario.objects.filter(bus=bus, fecha=fecha, hora_partida=hora_partida).exists():
            messages.error(request, "El bus ya tiene asignado un horario para esa fecha y hora de partida.")
            return redirect('nuevoHorario')

        # Validaciones adicionales
        if not costo_pasaje or float(costo_pasaje) <= 0:
            messages.error(request, "El costo del pasaje debe ser mayor a cero.")
            return redirect('nuevoHorario')

        # Guarda el nuevo horario
        Horario.objects.create(
            ruta=ruta,
            bus=bus,
            fecha=fecha,
            hora_partida=hora_partida,
            hora_llegada=hora_llegada,
            costo_pasaje=float(costo_pasaje)
        )
        messages.success(request, "Horario guardado exitosamente.")
        return redirect('listadoHorarios')
    else:
        return redirect('nuevoHorario')

def eliminarHorario(request,id):
    horarioEliminar=Horario.objects.get(id=id)
    horarioEliminar.delete()
    messages.success(request,"Horario eliminado Exitosamente")
    return redirect('/listadoHorarios')

def editarHorario(request, id):
    try:
        # Busca el horario con el ID proporcionado
        horarioEditar = Horario.objects.get(id=id)
        rutas = Ruta.objects.all()  # Para mostrar las rutas disponibles
        buses = Bus.objects.all()  # Para mostrar los buses disponibles
        return render(request, "editarHorario.html", {
            'horario': horarioEditar,
            'rutas': rutas,
            'buses': buses
        })
    except Horario.DoesNotExist:
        # Si el horario no existe, muestra un mensaje de error y redirige al listado
        messages.error(request, "El horario especificado no existe.")
        return redirect('listadoHorarios')

def procesarEdicionHorario(request):
    if request.method == 'POST':
        horario_id = request.POST.get('id')  # ID del horario a editar
        try:
            # Buscar el horario
            horario = Horario.objects.get(id=horario_id)
        except Horario.DoesNotExist:
            messages.error(request, "El horario especificado no existe.")
            return redirect('listadoHorarios')

        # Recuperar valores del formulario
        ruta_id = request.POST.get('ruta')  # ID de la nueva ruta
        bus_id = request.POST.get('bus')  # ID del nuevo bus
        fecha = request.POST.get('fecha')  # Nueva fecha
        hora_partida = request.POST.get('hora_partida')  # Nueva hora de partida
        hora_llegada = request.POST.get('hora_llegada')  # Nueva hora de llegada
        costo_pasaje = request.POST.get('costo_pasaje')  # Nuevo costo del pasaje

        # Validaciones de campos
        if not ruta_id or not bus_id or not fecha or not hora_partida or not hora_llegada or not costo_pasaje:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('editar_horario', id=horario_id)

        try:
            # Actualizar ruta y bus
            horario.ruta = Ruta.objects.get(id=ruta_id)
            horario.bus = Bus.objects.get(id=bus_id)
        except (Ruta.DoesNotExist, Bus.DoesNotExist):
            messages.error(request, "La ruta o el bus seleccionados no existen.")
            return redirect('editar_horario', id=horario_id)

        # Validar costo del pasaje
        try:
            costo_pasaje = float(costo_pasaje)
            if costo_pasaje <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, "El costo del pasaje debe ser un número mayor a cero.")
            return redirect('editar_horario', id=horario_id)

        # Actualizar los campos del horario
        horario.fecha = fecha
        horario.hora_partida = hora_partida
        horario.hora_llegada = hora_llegada
        horario.costo_pasaje = costo_pasaje
        horario.save()

        # Confirmar éxito
        messages.success(request, "Horario actualizado exitosamente.")
        return redirect('listadoHorarios')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('listadoHorarios')


        #Clientes

def nuevoCliente(request):
    return render(request, 'nuevoCliente.html')

def listadoClientes(request):
    # Obtiene el término de búsqueda del formulario
    query = request.GET.get('q', '')  # Usa el parámetro 'q' para el término de búsqueda
    if query:
        # Filtra clientes por nombre, apellido o DNI
        clientes = Cliente.objects.filter(
            nombre__icontains=query
        ) | Cliente.objects.filter(
            apellido__icontains=query
        ) | Cliente.objects.filter(
            dni__icontains=query
        )
    else:
        # Si no hay término de búsqueda, devuelve todos los clientes
        clientes = Cliente.objects.all()

    return render(request, 'listadoClientes.html', {'clientes': clientes, 'query': query})

def guardarCliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('txt_nombre')
        apellido = request.POST.get('txt_apellido')
        dni = request.POST.get('txt_dni')
        telefono = request.POST.get('txt_telefono')
        email = request.POST.get('txt_email')
        foto=request.FILES.get("txt_foto")

        # Verifica si ya existe un cliente con el mismo DNI
        if Cliente.objects.filter(dni=dni).exists():
            messages.error(request, "Ya existe un cliente con el DNI proporcionado.")
            return redirect('nuevoCliente')

        # Verifica si ya existe un cliente con el mismo email (si se proporcionó)
        if email and Cliente.objects.filter(email=email).exists():
            messages.error(request, "El correo proporcionado ya está registrado con otro cliente.")
            return redirect('nuevoCliente')

        # Guarda el nuevo cliente
        Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            telefono=telefono,
            email=email,
            foto=foto
        )
        messages.success(request, "Cliente guardado exitosamente.")
        return redirect('listadoClientes')
    else:
        return redirect('nuevoCliente')

def eliminarCliente(request,id):
    clienteEliminar=Cliente.objects.get(id=id)
    clienteEliminar.delete()
    messages.success(request,"Cliente eliminado Exitosamente")
    return redirect('/listadoClientes')

def editarCliente(request, id):
    try:
        # Busca el cliente con el ID proporcionado
        clienteEditar = Cliente.objects.get(id=id)
        return render(request, "editarCliente.html", {
            'cliente': clienteEditar
        })
    except Cliente.DoesNotExist:
        # Si el cliente no existe, muestra un mensaje de error y redirige al listado
        messages.error(request, "El cliente especificado no existe.")
        return redirect('listadoClientes')

def procesarEdicionCliente(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('id')
        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            messages.error(request, "El cliente especificado no existe.")
            return redirect('listadoClientes')

        # Recupera los valores del formulario
        nombre = request.POST.get('txt_nombre')
        apellido = request.POST.get('txt_apellido')
        dni = request.POST.get('txt_dni')
        telefono = request.POST.get('txt_telefono')
        email = request.POST.get('txt_email')

        # Validaciones
        if not nombre or not apellido or not dni:
            messages.error(request, "Los campos Nombre, Apellido y DNI son obligatorios.")
            return redirect('editar_cliente', id=cliente_id)

        # Verifica si el DNI ya existe en otro cliente
        if Cliente.objects.filter(dni=dni).exclude(id=cliente_id).exists():
            messages.error(request, "Ya existe un cliente con el mismo DNI.")
            return redirect('editar_cliente', id=cliente_id)

        # Actualiza los datos del cliente
        cliente.nombre = nombre
        cliente.apellido = apellido
        cliente.dni = dni
        cliente.telefono = telefono
        cliente.email = email
        cliente.save()

        messages.success(request, "Cliente actualizado exitosamente.")
        return redirect('listadoClientes')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('listadoClientes')
    

        #Vender

def venderPasaje(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')  # ID del cliente
        horario_id = request.POST.get('horario')  # ID del horario
        cantidad = int(request.POST.get('cantidad'))  # Cantidad de pasajes

        # Validaciones básicas
        if cantidad <= 0:
            messages.error(request, "La cantidad debe ser mayor a cero.")
            return redirect('venderPasaje')

        try:
            cliente = Cliente.objects.get(id=cliente_id)
            horario = Horario.objects.get(id=horario_id)
        except (Cliente.DoesNotExist, Horario.DoesNotExist):
            messages.error(request, "El cliente o el horario seleccionado no existe.")
            return redirect('venderPasaje')

        # Calcular los asientos disponibles correctamente
        asientos_ocupados = Pasaje.objects.filter(horario=horario).values_list('asientos', flat=True)
        asientos_ocupados = [int(a) for sublist in asientos_ocupados for a in sublist.split(',')]
        asientos_disponibles = sorted(list(set(range(1, horario.bus.capacidad + 1)) - set(asientos_ocupados)))

        if len(asientos_disponibles) < cantidad:
            # Mostrar mensaje de error con asientos restantes
            messages.error(request, f"No hay suficientes asientos disponibles. Asientos restantes: {len(asientos_disponibles)}")
            return redirect('venderPasaje')

        # Asignar asientos correctamente
        asientos = asientos_disponibles[:cantidad]
        total = horario.costo_pasaje * cantidad

        # Registrar la venta
        Pasaje.objects.create(
            cliente=cliente,
            horario=horario,
            cantidad=cantidad,
            total=total,
            asientos=",".join(map(str, asientos))
        )

        messages.success(request, f"Pasaje vendido exitosamente. Total: S/ {total:.2f}")
        return redirect('listadoPasajes')
    else:
        # Mostrar formulario para vender pasajes
        clientes = Cliente.objects.all()
        horarios = Horario.objects.all()
        return render(request, "venderPasaje.html", {'clientes': clientes, 'horarios': horarios})



def listadoPasajes(request):
    # Filtrar por rango de fechas si se proporcionan
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    pasajes = Pasaje.objects.all().select_related('cliente', 'horario').order_by('-fecha_compra')

    if fecha_inicio and fecha_fin:
        pasajes = pasajes.filter(fecha_compra__date__range=[fecha_inicio, fecha_fin])

    return render(request, "listadoPasajes.html", {
        'pasajes': pasajes,
        'today': now(),
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })

from django.http import HttpResponse
from django.shortcuts import redirect
import csv
from django.contrib import messages
from .models import Pasaje

def descargarReporte(request):
    # Obtener el tipo de reporte desde los parámetros GET
    tipo_reporte = request.GET.get('tipo_reporte')

    # Validar si se seleccionó una opción
    if not tipo_reporte:
        messages.error(request, "Seleccione un tipo de reporte.")
        return redirect('listadoPasajes')

    # Calcular el rango de fechas basado en el tipo de reporte
    fecha_fin = datetime.now().date()
    if tipo_reporte == 'dia':
        fecha_inicio = fecha_fin
    elif tipo_reporte == 'semana':
        fecha_inicio = fecha_fin - timedelta(days=7)
    elif tipo_reporte == 'mes':
        fecha_inicio = fecha_fin - timedelta(days=30)
    else:
        messages.error(request, "Tipo de reporte inválido.")
        return redirect('listadoPasajes')

    # Filtrar pasajes por el rango de fechas
    pasajes = Pasaje.objects.filter(fecha_compra__date__range=(fecha_inicio, fecha_fin))

    # Crear el archivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_pasajes.csv"'

    writer = csv.writer(response)
    writer.writerow(['Cliente', 'Horario', 'Asientos', 'Cantidad', 'Total', 'Fecha de Compra'])
    for pasaje in pasajes:
        writer.writerow([
            f"{pasaje.cliente.nombre} {pasaje.cliente.apellido}",
            f"{pasaje.horario.ruta.origen} -> {pasaje.horario.ruta.destino}",
            pasaje.asientos,
            pasaje.cantidad,
            pasaje.total,
            pasaje.fecha_compra,
        ])

    return response



def nuevaFactura(request):
    if request.method == 'POST':
        pasaje_id = request.POST.get('pasaje_id')  # ID del pasaje seleccionado

        # Validar que el pasaje exista
        try:
            pasaje = Pasaje.objects.get(id=pasaje_id)
        except Pasaje.DoesNotExist:
            messages.error(request, "El pasaje seleccionado no existe.")
            return redirect('listadoPasajes')

        # Validar si el pasaje ya tiene una factura asociada
        if Factura.objects.filter(pasajes=pasaje).exists():
            messages.error(request, "El pasaje ya tiene una factura generada.")
            return redirect('listadoPasajes')

        # Crear la factura para el pasaje
        factura = Factura.objects.create(
            cliente=pasaje.cliente,
            total=pasaje.total
        )
        factura.pasajes.add(pasaje)
        factura.save()

        # Redirigir al detalle de la factura
        return redirect('detalleFactura', factura_id=factura.id)
    else:
        return redirect('listadoPasajes')
    
def detalleFactura(request, factura_id):
    try:
        # Buscar la factura por su ID
        factura = Factura.objects.get(id=factura_id)
    except Factura.DoesNotExist:
        # Manejar el caso en el que no se encuentre la factura
        messages.error(request, "La factura solicitada no existe.")
        return redirect('listadoPasajes')

    # Renderizar la plantilla de detalle de la factura
    return render(request, "detalleFactura.html", {'factura': factura})

def descargarFactura(request, factura_id):
    try:
        # Obtener la factura
        factura = Factura.objects.get(id=factura_id)
    except Factura.DoesNotExist:
        return HttpResponse("La factura no existe.", status=404)

    # Crear el archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{factura.id}.pdf"'

    # Generar el contenido del PDF
    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    # Encabezado
    p.drawString(50, 800, f"Factura ID: {factura.id}")
    p.drawString(50, 780, f"Cliente: {factura.cliente.nombre} {factura.cliente.apellido}")
    p.drawString(50, 760, f"Fecha de emisión: {factura.fecha_emision.strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(50, 740, f"Total: S/ {factura.total}")

    # Detalle de los pasajes
    p.drawString(50, 720, "Detalle de Pasajes:")
    y = 700
    for pasaje in factura.pasajes.all():
        p.drawString(50, y, f"- Horario: {pasaje.horario.ruta.origen} -> {pasaje.horario.ruta.destino}")
        p.drawString(50, y - 20, f"  Asientos: {pasaje.asientos} | Cantidad: {pasaje.cantidad} | Total: S/ {pasaje.total}")
        y -= 40

    # Pie de página
    p.drawString(50, y - 20, "Gracias por su compra.")
    p.showPage()
    p.save()

    return response
