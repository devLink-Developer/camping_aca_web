"""
Vista para servir archivos media en producción
"""
from django.http import FileResponse, Http404
from django.conf import settings
from pathlib import Path


def serve_media(request, path):
    """Sirve archivos media en producción"""
    try:
        media_root = Path(settings.MEDIA_ROOT).resolve()
        # Resolve links before checking containment: an otherwise valid media
        # path may point to a file or directory outside the public media tree.
        file_path = (media_root / path).resolve()
        file_path.relative_to(media_root)
        if '..' in Path(path).parts or not file_path.is_file():
            raise Http404("Archivo no encontrado")
        media_file = file_path.open('rb')
    except (OSError, ValueError, RuntimeError) as error:
        raise Http404("Archivo no encontrado") from error

    return FileResponse(media_file)
