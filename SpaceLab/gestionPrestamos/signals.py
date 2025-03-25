from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from gestionPrestamos.models import Prestamo, Disponibilidad

@receiver(m2m_changed, sender=Prestamo.articulos.through)
def actualizar_disponibilidad(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':  # Solo cuando se agregan artículos al préstamo
        print(f"Se agregaron artículos al préstamo {instance.id}.")
        disponibilidad_prestamo = Disponibilidad.objects.get(nombre='En préstamo')
        for articulo_id in pk_set:
            articulo = instance.articulos.model.objects.get(pk=articulo_id)
            print(f"Actualizando disponibilidad del artículo {articulo.nombre}")
            articulo.disponibilidad = disponibilidad_prestamo
            articulo.save()
        print("Disponibilidad actualizada para los artículos agregados.")

