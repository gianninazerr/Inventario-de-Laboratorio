from django.contrib import admin
from gestionPrestamos.models import Publico, Categoria, Articulo, Laboratorio, Disponibilidad, Prestamo
from django.urls import reverse
from django.http import HttpResponseRedirect

admin.site.site_header = "Gestión de Inventario"
admin.site.site_title = "Administración de Inventario"
admin.site.index_title = "Bienvenido al Sistema de Gestión de Inventario"

# Register your models here.

# Para agregar buscadores:
class PublicoAdmin(admin.ModelAdmin):
    list_display=("nombre", "get_categoria", "lugar_de_trabajo", "email")
    search_fields=("nombre", "lugar_de_trabajo" )
    list_filter=("categoria",)

    def get_categoria(self, obj):
        return obj.categoria.nombre
    get_categoria.admin_order_field  = 'categoria'  #Allows column order sorting
    get_categoria.short_description = 'Categoria'  #Renames column head

class CategoriaAdmin(admin.ModelAdmin):
    list_display=("nombre",)
    search_fields=("nombre", )

class ArticuloAdmin(admin.ModelAdmin):
    list_display=("id","nombre","descripcion","marca", "modelo","serie","tipo","numero", "estado", "get_laboratorio","get_disponibilidad")
    list_filter=("laboratorio","disponibilidad","marca")
    search_fields=("id","nombre", "descripcion","marca","modelo" )

    actions = ['crear_prestamo']
    def crear_prestamo(self, request, queryset):
        # Obtiene los IDs de los artículos seleccionados
        ids = ",".join(str(articulo.id) for articulo in queryset)      
        # Redirige al formulario de creación de préstamos con los IDs en la URL
        url = reverse('admin:gestionPrestamos_prestamo_add') + f"?articulos={ids}"
        return HttpResponseRedirect(url)
    crear_prestamo.short_description = "Crear préstamo con los artículos seleccionados"

    def get_laboratorio(self, obj):
        return obj.laboratorio.nombre
    get_laboratorio.admin_order_field  = 'laboratorio'  #Allows column order sorting
    get_laboratorio.short_description = 'Laboratorio'  #Renames column head

    def get_disponibilidad(self, obj):
        return obj.disponibilidad.nombre
    get_disponibilidad.admin_order_field  = 'disponibilidad'  #Allows column order sorting
    get_disponibilidad.short_description = 'Disponibilidad'  #Renames column head
 

class LaboratorioAdmin(admin.ModelAdmin):
    list_display=("nombre",)

class DisponibilidadAdmin(admin.ModelAdmin):
    list_display=("nombre",)


class PrestamoAdmin(admin.ModelAdmin):
    list_display = ("get_articulos", "get_publico", "get_lugar_de_trabajo", "fecha_entrega", "fecha_devolucion", "devolucion")
    list_filter = ("fecha_entrega", "devolucion", "publico__lugar_de_trabajo")
    date_hierarchy = "fecha_entrega"
    search_fields = ("articulos__nombre", "publico__nombre", "publico__lugar_de_trabajo")

    def get_articulos(self, obj):
        return ", ".join([articulo.nombre for articulo in obj.articulos.all()])
    get_articulos.short_description = 'Articulos'

    def get_publico(self, obj):
        return obj.publico.nombre
    get_publico.admin_order_field = 'publico__nombre'
    get_publico.short_description = 'Nombre usuario'

    def get_lugar_de_trabajo(self, obj):
        return obj.publico.lugar_de_trabajo
    get_lugar_de_trabajo.admin_order_field = 'publico__lugar_de_trabajo'
    get_lugar_de_trabajo.short_description = 'Lugar de trabajo'

    def get_changeform_initial_data(self, request):
        #Preselecciona los artículos cuando se llega a la página de creación de préstamos desde la acción en la vista de Artículos.
        articulo_ids = request.GET.get("articulos")
        if articulo_ids:
            return {"articulos": Articulo.objects.filter(id__in=articulo_ids.split(","))}     
        return super().get_changeform_initial_data(request)

    actions = ['devolucion']
    # Actualiza el campo 'devolucion' a True
    def devolucion(modeladmin, request, queryset):
        queryset.update(devolucion=True)
    # Actualiza la disponibilidad de los artículos asociados
        for prestamo in queryset:
            for articulo in prestamo.articulos.all():
                articulo.disponibilidad = Disponibilidad.objects.get(nombre='Disponible')
                articulo.save()
    devolucion.short_description = "Realizar devolución"

admin.site.register(Publico, PublicoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Articulo, ArticuloAdmin)
admin.site.register(Laboratorio, LaboratorioAdmin)
admin.site.register(Disponibilidad, DisponibilidadAdmin)
admin.site.register(Prestamo, PrestamoAdmin)
