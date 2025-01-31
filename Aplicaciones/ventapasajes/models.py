from django.db import models

# Create your models here.
class Bus(models.Model):
    id = models.AutoField(primary_key=True) 
    placa = models.CharField(max_length=10, unique=True)  # Placa única
    modelo = models.CharField(max_length=50)             # Modelo del bus
    capacidad = models.PositiveIntegerField()            # Capacidad máxima de pasajeros

    def __str__(self):
        return f"{self.placa} - {self.modelo} (Capacidad: {self.capacidad})"
    

class Conductor(models.Model):
    id = models.AutoField(primary_key=True)  
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=10, unique=True)   # Documento de identidad único
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    bus = models.OneToOneField(Bus, on_delete=models.CASCADE)  # Relación uno a uno con Bus

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.dni}"


class Ruta(models.Model):
    id = models.AutoField(primary_key=True)
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.origen} -> {self.destino}"
    

class Horario(models.Model):
    id = models.AutoField(primary_key=True)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)  # Relación con la ruta
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)    # Relación con el bus
    fecha = models.DateField()                                # Fecha del viaje
    hora_partida = models.TimeField()                         # Hora de salida
    hora_llegada = models.TimeField()                         # Hora de llegada
    costo_pasaje = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Costo del pasaje

    def __str__(self):
        return f"{self.ruta} - {self.fecha} ({self.hora_partida} a {self.hora_llegada})"
    

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)              # Clave primaria auto incremental
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=10, unique=True)    # Documento de identidad único
    telefono = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)     # Opcional
    foto=models.FileField(upload_to='clientes',null=True,blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.dni}"   

class Pasaje(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Cliente que compra el pasaje
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)  # Horario del viaje
    fecha_compra = models.DateTimeField(auto_now_add=True)          # Fecha y hora de compra
    cantidad = models.PositiveIntegerField(default=1)               # Número de pasajes
    total = models.DecimalField(max_digits=10, decimal_places=2)    # Costo total de los pasajes
    asientos = models.CharField(max_length=255)                     # Números de asientos separados por comas

    def __str__(self):
        return f"Pasaje de {self.cliente} para {self.horario}"

    
class Factura(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria auto incremental
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Cliente asociado
    pasajes = models.ManyToManyField(Pasaje)  # Pasajes relacionados con la factura
    fecha_emision = models.DateTimeField(auto_now_add=True)  # Fecha de emisión
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Monto total de la factura

    def __str__(self):
        return f"Factura {self.id} - Cliente: {self.cliente.nombre} {self.cliente.apellido}"



