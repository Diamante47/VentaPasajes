from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('administrador/', views.administrador, name='administrador'),

    #Buses
    path('nuevoBus/', views.nuevoBus, name='nuevoBus'),  # Formulario para crear un nuevo bus
    path('listadoBuses/', views.listadoBuses, name='listadoBuses'),  # Listado de buses
    path('guardarBus/', views.guardarBus, name='guardarBus'),
    path('eliminarBus/<int:id>/', views.eliminarBus, name='eliminarBus'),
    path('editarBus/<int:id>/', views.editarBus, name='editar_bus'),
    path('procesarEdicionBus/', views.procesarEdicionBus, name='procesar_edicion_bus'),

    #Conductores
    path('nuevoConductor/', views.nuevoConductor, name='nuevoConductor'),  # Formulario para crear un nuevo bus
    path('listadoConductores/', views.listadoConductores, name='listadoConductores'), 
    path('guardarConductor/', views.guardarConductor, name='guardarConductor'),
    path('eliminarConductor/<int:id>/', views.eliminarConductor, name='eliminarConductor'),
    path('editarConductor/<int:id>/', views.editarConductor, name='editar_conductor'),
    path('procesarEdicionConductor/', views.procesarEdicionConductor, name='procesar_edicion_conductor'),

    #Rutas
    path('nuevaRuta/', views.nuevaRuta, name='nuevaRuta'),  # Formulario para crear un nuevo bus
    path('listadoRutas/', views.listadoRutas, name='listadoRutas'), 
    path('guardarRuta/', views.guardarRuta, name='guardarRuta'),
    path('eliminarRuta/<int:id>/', views.eliminarRuta, name='eliminarRuta'),
    path('editarRuta/<int:id>/', views.editarRuta, name='editar_Ruta'),
    path('procesarEdicionRuta/', views.procesarEdicionRuta, name='procesar_edicion_ruta'),

    #Horarios
    path('nuevoHorario/', views.nuevoHorario, name='nuevoHorario'),  # Formulario para crear un nuevo bus
    path('listadoHorarios/', views.listadoHorarios, name='listadoHorarios'), 
    path('guardarHorario/', views.guardarHorario, name='guardarHorario'),
    path('eliminarHorario/<int:id>/', views.eliminarHorario, name='eliminarHorario'),
    path('editarHorario/<int:id>/', views.editarHorario, name='editar_horario'),
    path('procesarEdicionHorario/', views.procesarEdicionHorario, name='procesar_edicion_horario'),

    #Cliente
    path('nuevoCliente/', views.nuevoCliente, name='nuevoCliente'),  # Formulario para crear un nuevo bus
    path('listadoClientes/', views.listadoClientes, name='listadoClientes'), 
    path('guardarCliente/', views.guardarCliente, name='guardarCliente'),
    path('eliminarCliente/<int:id>/', views.eliminarCliente, name='eliminarCliente'),
    path('editarCliente/<int:id>/', views.editarCliente, name='editar_cliente'),
    path('procesarEdicionCliente/', views.procesarEdicionCliente, name='procesar_edicion_cliente'),

    #Pasaje
    path('venderPasaje/', views.venderPasaje, name='venderPasaje'),  # URL para vender pasajes
    path('listadoPasajes/', views.listadoPasajes, name='listadoPasajes'),
    path('descargarReporte/', views.descargarReporte, name='descargarReporte'),

    #Factura
    path('nuevaFactura/', views.nuevaFactura, name='nuevaFactura'),
    path('detalleFactura/<int:factura_id>/', views.detalleFactura, name='detalleFactura'),
    path('descargarFactura/<int:factura_id>/', views.descargarFactura, name='descargarFactura'),

]