"""Polish public copy only in the explicitly cloned DevLink review database."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


def main():
    import django
    django.setup()
    from django.conf import settings
    from django.contrib.auth import get_user_model
    from django.db import transaction
    from apps.landing.models import FAQ, News, PriceCategory, Service, SiteConfiguration

    if settings.DATABASES['default']['NAME'] != 'camping_aca_devlink':
        raise RuntimeError('This script is restricted to the cloned DevLink review database.')

    with transaction.atomic():
        SiteConfiguration.objects.update(
            hero_image='', hero_focus_x=50, hero_focus_y=50,
            opening_hours='Miércoles a lunes, de 10 a 18',
            phone='+54 9 11 6649 9440', email='campingacalujaninfo@gmail.com',
        )
        SiteConfiguration.objects.filter(special_alert='MARTES CERRADO').update(
            special_alert='Los martes el predio permanece cerrado.'
        )
        # Preserve historical values, but do not present them as current rates.
        PriceCategory.objects.update(is_active=False)
        faqs = [
            ('MARTES CERRADO', '¿Qué días y horarios abre el camping?',
             'De miércoles a lunes, de 10 a 18. Los martes permanece cerrado.'),
            ('TENGO QUE RESERVAR?', '¿Hace falta reservar?',
             'Podés venir sin reservar para pasar el día. Para una visita en grupo, consultanos antes de venir.'),
            ('PUEDO LLEVAR MASCOTAS?', '¿Puedo llevar mascotas?',
             'No se permite el ingreso de mascotas, para cuidar la convivencia y la fauna del predio.'),
            ('TENGO QUE SER SOCIO DEL ACA?', '¿Necesito ser socio del ACA?',
             'Podés ingresar como socio del ACA o como invitado de un socio.'),
        ]
        for old, question, answer in faqs:
            FAQ.objects.filter(question=old).update(question=question, answer=answer)
        Service.objects.filter(title='Servicios Adicionales').update(
            title='Servicios adicionales', description='Comodidades para disfrutar tu estadía.'
        )
        Service.objects.filter(title='Camping y Recreación').update(title='Camping y recreación')
        copy = [
            ('Pileta Abierta!', 'Pileta y descanso',
             'Un plan para disfrutar al aire libre, rodeado por el bosque. Consultá la disponibilidad y los horarios de pileta de la temporada antes de venir.'),
            ('Alquiler de bicicletas!', 'Paseos en bicicleta',
             'Recorré las 25 hectáreas del predio a tu ritmo. Consultá por el alquiler de bicicletas y encontrá tu rincón para compartir unos mates.'),
            ('Canchas!', 'Deportes al aire libre',
             'Fútbol, vóley, pádel o tenis: elegí tu plan para compartir. Consultá la disponibilidad de las canchas para organizar tu visita.'),
        ]
        for old, title, description in copy:
            News.objects.filter(title=old).update(title=title, description=description)
        # This changes the clone only, and only if the copied account still uses
        # the legacy predictable password. Other accounts remain untouched.
        admin = get_user_model().objects.filter(username='admin').first()
        if admin and admin.check_password('admin123'):
            admin.set_unusable_password()
            admin.save(update_fields=['password'])
            print('Legacy default administrator disabled in the review copy.')
    print('DevLink review copy prepared; original database and media are unchanged.')


if __name__ == '__main__':
    main()
