from django.db import models

# Create your models here.

from datetime import datetime, timedelta

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100, blank=True ,null=True )
    isbn = models.CharField(max_length=20, blank=True ,null=True )
    editorial = models.CharField(max_length=100, blank=True ,null=True )
    fecha_publicacion = models.DateField( blank=True ,null=True )
    num_paginas = models.IntegerField( blank=True ,null=True )
    avatar= models.ImageField(upload_to='libros',null=True )
    def __str__(self):
        return self.titulo
    

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
    
    def __str__(self):
        return self.libro.titulo

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

class Prestamo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(blank=True ,null=True )
    
    opciones_estado = [
        (True, 'Si'),
        (False, 'No'),
    ]
    devuelto =models.BooleanField(blank=True ,null=True, max_length=10, choices=opciones_estado, default=False, )
    
    
    # fecha_devolucion_real = models.DateField()

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
        