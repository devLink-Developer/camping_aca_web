"""Prepare and serve the landing with an isolated local SQLite database."""
import argparse
import os
import sys
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_local'


def seed_preview():
    """Reuse public seed content without publishing its historical prices."""
    from django.conf import settings
    from django.core.management import call_command
    from django.db import connection, transaction
    from apps.landing.models import FAQ, GalleryImage, Price, PriceCategory, SiteConfiguration, Testimonial

    if connection.vendor != 'sqlite':
        raise RuntimeError('Preview seeding is restricted to SQLite.')

    with transaction.atomic():
        # Keep all legacy pricing invisible: it is removed in the same transaction.
        call_command('load_initial_data', verbosity=0, stdout=StringIO(), stderr=StringIO())
        Price.objects.all().delete()
        PriceCategory.objects.update(is_active=False)
        Testimonial.objects.all().delete()
        config = SiteConfiguration.get_config()
        SiteConfiguration.objects.filter(pk=config.pk).update(
            hero_image='',
            phone='+54 9 11 6649 9440',
            email='campingacalujaninfo@gmail.com',
            facebook_url='https://facebook.com/campingacalujan',
            instagram_url='https://instagram.com/campingacalujan/',
            special_alert='Consultá horarios y tarifas vigentes antes de tu visita.',
            is_alert_active=True,
        )

        # Public information confirmed on the campsite's official information page.
        faqs = [
            ('MARTES CERRADO', '¿Qué días y horarios abre el camping?', 'De miércoles a lunes, de 10 a 18. Los martes permanece cerrado.'),
            ('TENGO QUE RESERVAR?', '¿Hace falta reservar?', 'No se requiere reserva previa para la visita general.'),
            ('PUEDO LLEVAR MASCOTAS?', '¿Puedo llevar mascotas?', 'No se permite el ingreso con mascotas.'),
            ('TENGO QUE SER SOCIO DEL ACA?', '¿Necesito ser socio del ACA?', 'Podés ingresar siendo socio del ACA o invitado de un socio.'),
        ]
        for order, (legacy_question, question, answer) in enumerate(faqs, start=1):
            FAQ.objects.update_or_create(question=question, defaults={'answer': answer, 'order': order})
            FAQ.objects.filter(question=legacy_question).delete()

        # Refer to the original files; bulk_create avoids image normalization.
        filenames = [
            ('001_orig.jpg', 'Mate bajo los árboles'),
            ('002_orig.jpg', 'Compartir en el bosque'),
            ('003_orig_1280x720.jpg', 'Proveeduría'),
            ('005_orig.jpg', 'Acampar'),
            ('006_orig_1280x720.jpg', 'Canchas'),
            ('012_orig.jpg', 'Tenis'),
            ('bici-2_orig.jpg', 'Bicicletas'),
            ('w-004_orig_1280x720.jpg', 'Senderos'),
            ('w-008_orig.jpg', 'Aves'),
        ]
        existing = set(GalleryImage.objects.values_list('image', flat=True))
        images = []
        for index, (filename, title) in enumerate(filenames, start=1):
            relative = f'gallery/{filename}'
            if relative in existing:
                GalleryImage.objects.filter(image=relative).update(title=title, alt_text=f'{title} en Camping ACA Luján', order=index)
            if relative not in existing and (settings.MEDIA_ROOT / relative).is_file():
                images.append(GalleryImage(
                    title=title,
                    alt_text=f'{title} en Camping ACA Luján',
                    image=relative,
                    order=index,
                ))
        GalleryImage.objects.bulk_create(images)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-only', action='store_true', help='Create the local schema and seed, then exit.')
    args = parser.parse_args()

    import django
    django.setup()
    from django.conf import settings
    from django.core.management import call_command

    database = settings.DATABASES['default']
    if database['ENGINE'] != 'django.db.backends.sqlite3' or Path(database['NAME']).resolve() != ROOT / 'db.preview.sqlite3':
        raise RuntimeError('Refusing to initialize a database outside the dedicated preview file.')

    call_command('check')
    call_command('migrate', run_syncdb=True, interactive=False)
    seed_preview()
    print('Local preview ready: http://127.0.0.1:8000/ (SQLite; console email; no remote database).')
    if not args.prepare_only:
        call_command('runserver', '127.0.0.1:8000', use_reloader=False)


if __name__ == '__main__':
    main()
