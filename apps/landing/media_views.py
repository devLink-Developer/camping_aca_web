"""
Vista para servir archivos media en producción
"""
from django.http import FileResponse, Http404
from django.conf import settings
import os


def serve_media(request, path):
    """Sirve archivos media en producción"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    if not os.path.exists(file_path):
        raise Http404("Archivo no encontrado")
    
    return FileResponse(open(file_path, 'rb'))
