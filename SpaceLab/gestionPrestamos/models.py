from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Categoria(models.Model):
    nombre=models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class Publico(models.Model):
    nombre=models.CharField(max_length=30)
    categoria=models.ForeignKey(Categoria, on_delete=models.CASCADE,db_constraint=False)
    lugar_de_trabajo=models.CharField(max_length=50)
    email=models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Laboratorio(models.Model):
    nombre=models.CharField(max_length=30)

    def __str__(self):
        return self.nombre
    
class Disponibilidad(models.Model):
    nombre=models.CharField(max_length=30)

    def __str__(self):
        return self.nombre
        
class Articulo(models.Model):
    #id=models.IntegerField()
    tipo=models.CharField(max_length=7)
    numero=models.IntegerField()
    nombre=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=75)
    marca=models.CharField(max_length=20)
    modelo=models.CharField(max_length=20)
    serie=models.CharField(max_length=10)
    estado=models.CharField(max_length=30)
    laboratorio=models.ForeignKey(Laboratorio, on_delete=models.CASCADE,db_constraint=False)
    disponibilidad=models.ForeignKey(Disponibilidad, on_delete=models.CASCADE,db_constraint=False)

    #def __str__(self):
      #  return self.descripcion


class Prestamo(models.Model):
    fecha_entrega=models.DateField()
    fecha_devolucion=models.DateField()
    devolucion=models.BooleanField()
    publico=models.ForeignKey(Publico, on_delete=models.CASCADE,db_constraint=False)
    articulos = models.ManyToManyField('Articulo', related_name='prestamo')
    



#post_save.connect(actualizar_disponibilidad, sender=Prestamo)
#esta linea me parece que no es necesaria

#    def save(self, *args, **kwargs):
#        if not self.id:
#            # Si es un nuevo préstamo, actualizamos el estado del artículo
#            self.articulo.disponibilidad.nombre = "En préstamo"
#            self.articulo.save()
#        super(Prestamo, self).save(*args, **kwargs)

#@receiver(post_save, sender=Prestamo)
#def update_articulo_estado(sender, instance, **kwargs):
#    if not instance.id:
#        # Si es un nuevo préstamo, actualizamos el estado del artículo
#        instance.articulo.disponibilidad.nombre = "En préstamo"
#        instance.articulo.save()