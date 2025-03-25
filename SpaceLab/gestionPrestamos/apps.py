from django.apps import AppConfig


class GestionprestamosConfig(AppConfig):
    name = "gestionPrestamos"

    def ready(self):
        import gestionPrestamos.signals 
