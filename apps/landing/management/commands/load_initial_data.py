from django.core.management.base import BaseCommand
from apps.landing.models import (
    Service, PriceCategory, Price, FAQ, SiteConfiguration
)


class Command(BaseCommand):
    help = 'Carga datos iniciales desde el HTML existente'

    def handle(self, *args, **options):
        self.stdout.write('Cargando datos iniciales...')
        
        # Crear configuración del sitio
        config = SiteConfiguration.get_config()
        config.site_name = 'Camping ACA Luján'
        config.tagline = 'Un lugar para vos'
        config.opening_hours = 'Miércoles a Lunes de 10 a 18 hs'
        config.special_alert = 'MARTES CERRADO'
        config.is_alert_active = True
        config.save()
        self.stdout.write(self.style.SUCCESS('✓ Configuración del sitio creada'))
        
        # Crear servicios
        services_data = [
            {
                'title': 'Camping y Recreación',
                'description': 'Instalaciones completas para acampar con comodidad',
                'features': [
                    'Parrillas', 'Toma de luz', 'Mesas y sillas',
                    'Piletas lava vajillas grupales', 'Duchas con agua caliente',
                    'Quinchos', 'Dos sectores de recreación',
                    'Cada sector con batería de baños completa'
                ],
                'order': 1
            },
            {
                'title': 'Deportes',
                'description': 'Múltiples canchas y espacios deportivos',
                'features': [
                    'Canchas de voley', 'Canchas de paddle', 'Cancha de tenis',
                    'Canchas de fútbol de 11 - 9 y 5', 'Piscina para grandes y chicos'
                ],
                'order': 2
            },
            {
                'title': 'Servicios Adicionales',
                'description': 'Todo lo que necesitas para una estadía perfecta',
                'features': [
                    'Proveeduría con elementos básicos',
                    'Servicios de comidas rápidas',
                    'Pantalla gigante para eventos',
                    'Salón de juegos (pool, ping pong, tejo, metegol)',
                    'Alquiler de bicicletas'
                ],
                'order': 3
            }
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                title=service_data['title'],
                defaults=service_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Servicio creado: {service.title}'))
        
        # Crear categorías de precios
        socios, _ = PriceCategory.objects.get_or_create(
            name='SOCIOS',
            defaults={'order': 1}
        )
        no_socios, _ = PriceCategory.objects.get_or_create(
            name='NO SOCIOS',
            defaults={'order': 2}
        )
        self.stdout.write(self.style.SUCCESS('✓ Categorías de precios creadas'))
        
        # Crear precios para socios
        socios_prices = [
            {
                'item_name': 'Para acampar',
                'description': 'Incluye el ingreso de 4 personas, 1 vehículo y una carpa, casa rodante, tráiler o motor home.',
                'amount': 28500.00,
                'order': 1
            },
            {
                'item_name': 'Adicionales',
                'description': '1 persona más, 1 vehículo No Socio más u otra carpa.',
                'amount': 9000.00,
                'order': 2
            },
            {
                'item_name': 'Pasar el día',
                'description': 'Vehiculo del socio sin cargo',
                'amount': 0,
                'is_free': True,
                'order': 3
            },
        ]
        
        for price_data in socios_prices:
            Price.objects.get_or_create(
                category=socios,
                item_name=price_data['item_name'],
                defaults=price_data
            )
        
        # Crear precios para no socios
        no_socios_prices = [
            {
                'item_name': 'Para acampar',
                'description': 'Incluye el ingreso de 4 personas, 1 vehículo y una carpa, casa rodante, tráiler o motor home.',
                'amount': 41000.00,
                'order': 1
            },
            {
                'item_name': 'Adicionales',
                'description': '1 persona más, 1 vehículo No Socio más u otra carpa.',
                'amount': 13000.00,
                'order': 2
            },
            {
                'item_name': 'Pasar el día',
                'description': 'Vehiculos adicionales $6.000,00',
                'amount': 6000.00,
                'order': 3
            },
        ]
        
        for price_data in no_socios_prices:
            Price.objects.get_or_create(
                category=no_socios,
                item_name=price_data['item_name'],
                defaults=price_data
            )
        
        self.stdout.write(self.style.SUCCESS('✓ Precios creados'))
        
        # Crear FAQs
        faqs_data = [
            {
                'question': 'MARTES CERRADO',
                'answer': 'Si necesitamos un día para reordenar, mejorar, y descansar. De esta forma podemos disfrutar del predio de Miércoles a Lunes de 10 hrs a 18 hrs.',
                'order': 1
            },
            {
                'question': 'TENGO QUE RESERVAR?',
                'answer': 'Lunes inclusive, de 10 hrs a 18 hrs. Vení y podrás disfrutar de las diferentes clases de Pájaros y Ardillas que habitan en el Predio. De los árboles, su belleza y su silencio.',
                'order': 2
            },
            {
                'question': 'PUEDO LLEVAR MASCOTAS?',
                'answer': 'POR LA CONVIVENCIA GENERAL, NO SE PUEDE ENTRAR CON MASCOTAS. Pensando en Todos los Visitantes, esta restringido el ingreso de animales. De esta forma podemos disfrutar de las diferentes clases de Pájaros y Ardillas que habitan en el Predio.',
                'order': 3
            },
            {
                'question': 'TENGO QUE SER SOCIO DEL ACA?',
                'answer': 'Puede ser Socio o Invitado de uno.',
                'order': 4
            },
        ]
        
        for faq_data in faqs_data:
            FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults=faq_data
            )
        
        self.stdout.write(self.style.SUCCESS('✓ FAQs creadas'))
        
        self.stdout.write(self.style.SUCCESS('\n¡Datos iniciales cargados exitosamente!'))
        self.stdout.write(self.style.WARNING('\nRecuerda:'))
        self.stdout.write('1. Subir imágenes de galería desde el admin')
        self.stdout.write('2. Configurar la imagen hero principal')
        self.stdout.write('3. Agregar testimonios de clientes')
        self.stdout.write('4. Configurar información de contacto en Configuración del Sitio')
