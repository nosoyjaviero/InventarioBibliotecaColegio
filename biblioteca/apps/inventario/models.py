from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete

from datetime import datetime, timedelta
from django.contrib import messages

#estas dos importaciones se añadieron cuando se añadio el metodo de restar un libro cuando se realiza el prestamo
#Estos son módulos de Django que se utilizan para crear señales y receptores de señales en el contexto de modelos de bases de datos.

# Las señales son una forma en que los componentes de Django pueden enviar y recibir mensajes entre sí de manera asíncrona. En este caso, el módulo "post_save" se utiliza para enviar una señal después de que se haya guardado un objeto de modelo en la base de datos.

# El módulo "receiver" se utiliza para crear un receptor de señales que escucha y responde a la señal enviada. En este caso, el receptor escucha la señal "post_save" y realiza alguna acción en respuesta al evento de guardar un objeto de modelo en la base de datos.

# En resumen, estos módulos se utilizan para crear una funcionalidad que se activa cuando se guarda un objeto de modelo en la base de datos. Por ejemplo, se podría utilizar esto para actualizar un contador de cuántas veces se ha guardado un objeto en particular, o para enviar un correo electrónico de confirmación después de que se haya guardado un objeto de modelo en la base de datos.

from django.db.models.signals import post_save
from django.dispatch import receiver


class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100, blank=True ,null=True )
    isbn = models.CharField(max_length=20, blank=True ,null=True )
    editorial = models.CharField(max_length=100, blank=True ,null=True )
    fecha_publicacion = models.DateField( blank=True ,null=True )
    num_paginas = models.IntegerField( blank=True ,null=True )
    avatar= models.ImageField('Imagen de Portada',upload_to='libros',null=True, blank=True )
    
    
    def __str__(self):
        return self.titulo    

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)    
    apellido = models.CharField(max_length=50)
    cedula = models.CharField(max_length=20, null=True)
    direccion = models.CharField(max_length=200, blank=True ,null=True )
    telefono = models.CharField(max_length=20 , blank=True ,null=True )    
    correo_electronico = models.EmailField( blank=True ,null=True )   
    seccion = models.CharField(max_length=20, null=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.seccion}"

class Ejemplar(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    opciones_estado = [
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('en_reparacion', 'En Reparación'),
        ('extraviado', 'Extraviado'),
    ]
    estado = models.CharField(max_length=20, choices=opciones_estado)
    ubicacion = models.CharField(max_length=100, blank=True ,null=True )
    fecha_adquisicion = models.DateField( blank=True ,null=True )
    ultima_revision = models.DateField( blank=True ,null=True )
    cantidad = models.IntegerField(default=1, blank=True ,null=True )
    comentarios=models.CharField(max_length=300, blank=True ,null=True )
    
    def __str__(self):
        return self.libro.titulo

    def set_disponible(self):
        self.estado = 'disponible'
        self.save()
    def set_no_disponible(self):
        self.estado = 'prestado'
        self.save()
    def incrementar_cantidad(self):
        self.cantidad += 1
        self.save()
    def restar_cantidad(self):
        self.cantidad -= 1
        self.save()


class Prestamo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField('Fecha Prestamo')
    fecha_devolucion = models.DateField('Fecha a devolver',blank=True ,null=True )
    
    opciones_estado = [
        (True, 'Si'),
        (False, 'No'),
    ]
    devuelto =models.BooleanField(blank=True ,null=True, max_length=10, choices=opciones_estado, default=False )
    
    def __str__(self):
        return self.libro.titulo

    def actualizar_cantidad_ejemplar(self):
        if self.ejemplar.cantidad == 0:
            # messages.error(self.request, "No hay ejemplares disponibles para prestar.")
            pass
            # self.ejemplar.set_no_disponible()
            # self.ejemplar.estado = 'prestado'
            # self.ejemplar.save()
            # raise ValidationError('No hay ejemplares disponibles para prestar.')
        else:
            self.ejemplar.cantidad -= 1
            self.ejemplar.save()
            if self.ejemplar.cantidad == 0:
                self.ejemplar.set_no_disponible()
    

# Este código crea una señal "post_save" que se activa cada vez que se guarda un objeto "Prestamo" en la base de datos. La señal está asociada con una función llamada "actualizar_cantidad_ejemplar" que se define en la clase "Prestamo" y se llama cada vez que se guarda un objeto "Prestamo" en la base de datos.

# La función "actualizar_cantidad_ejemplar" se encarga de actualizar la cantidad de ejemplares disponibles en un objeto relacionado "Ejemplar". El método disminuye la cantidad de ejemplares disponibles en uno cada vez que se guarda un objeto "Prestamo". Esto se logra restando 1 del campo "cantidad" del objeto "Ejemplar" relacionado con el objeto "Prestamo" actual y guardando los cambios en la base de datos mediante el método "save()".

# El decorador "@receiver" se utiliza para conectar la señal "post_save" con la función "actualizar_cantidad_ejemplar" que se define en la clase "Prestamo". La señal "post_save" es enviada por Django cada vez que se guarda un objeto "Prestamo" en la base de datos, y luego se llama a la función "actualizar_cantidad_ejemplar" para actualizar la cantidad de ejemplares disponibles en el objeto "Ejemplar" relacionado con el objeto "Prestamo".

# En resumen, este código define una señal que se activa cada vez que se guarda un objeto "Prestamo" en la base de datos, y utiliza una función para actualizar la cantidad de ejemplares disponibles en un objeto relacionado "Ejemplar" cada vez que se guarda un objeto "Prestamo". Esto permite mantener actualizada la cantidad de ejemplares disponibles en la base de datos y evitar que se presten más ejemplares de los disponibles.

    def save(self, *args, **kwargs):
        if not self.fecha_devolucion:
            self.fecha_devolucion = datetime.now().date() + timedelta(days=15)
        return super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.ejemplar.libro.titulo} - {self.usuario.nombre} {self.usuario.apellido}"

    @property
    def esta_atrasado(self):
        if not self.fecha_devolucion_real and self.fecha_devolucion < datetime.now().date():
            return True
        return False

    @property
    def estado_devolucion(self):
        if self.fecha_devolucion_real:
            return "Devuelto"
        elif self.esta_atrasado:
            return "Atrasado"
        else:
            return "En préstamo"

class Multa(models.Model):
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE)
    fecha_emision = models.DateField()
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    opciones_estado = [
        ('pagado', 'Pagado'),
        ('no_pagado', 'No Pagado'),
    ]
    estado = models.CharField(max_length=10, choices=opciones_estado)
    
    def __str__(self):
        return f"{self.prestamo.usuario} - Estado: {self.estado} Libro:{self.prestamo.ejemplar.libro}" 
        
        
# @receiver(models.signals.post_save, sender=Prestamo)
# def actualizar_cantidad_ejemplar(sender, instance, **kwargs):
#     instance.actualizar_cantidad_ejemplar()
            
# @receiver(post_delete, sender=Prestamo)
# def actualizar_ejemplar(sender, instance, **kwargs):
#     ejemplar = instance.ejemplar
#     ejemplar.incrementar_cantidad()
#     if ejemplar.cantidad > 0:
#         ejemplar.set_disponible()