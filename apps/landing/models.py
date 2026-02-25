from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.files.base import ContentFile

from io import BytesIO
import os

from PIL import Image, ImageOps, ImageFilter


class Lead(models.Model):
    """Leads capturados para campaña de cumpleaños"""
    
    # Datos personales
    full_name = models.CharField('Nombre Completo', max_length=200)
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Teléfono', max_length=50)
    dni = models.CharField('DNI', max_length=20, blank=True)
    birth_date = models.DateField('Fecha de Cumpleaños')
    
    # Marketing
    accepts_marketing = models.BooleanField('Acepta Marketing', default=True, 
                                           help_text='Acepta recibir promociones y ofertas')
    
    # Control
    created_at = models.DateTimeField('Registrado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)
    ip_address = models.GenericIPAddressField('IP', blank=True, null=True)
    source = models.CharField('Fuente', max_length=50, default='qr_birthday', 
                             help_text='qr_birthday, web_form, etc')
    
    # Voucher generado
    birthday_voucher = models.ForeignKey('vouchers.Voucher', on_delete=models.SET_NULL, 
                                        null=True, blank=True, related_name='lead',
                                        verbose_name='Voucher de Cumpleaños')
    voucher_sent = models.BooleanField('Voucher Enviado', default=False)
    voucher_sent_date = models.DateTimeField('Fecha Envío Voucher', blank=True, null=True)
    
    # Notas
    notes = models.TextField('Notas', blank=True)
    
    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['birth_date']),
            models.Index(fields=['voucher_sent']),
        ]
    
    def __str__(self):
        return f"{self.full_name} - {self.email}"
    
    def days_until_birthday(self):
        """Calcula días hasta el próximo cumpleaños"""
        today = timezone.now().date()
        next_birthday = self.birth_date.replace(year=today.year)
        
        # Si ya pasó este año, calcular para el próximo
        if next_birthday < today:
            next_birthday = self.birth_date.replace(year=today.year + 1)
        
        delta = next_birthday - today
        return delta.days
    
    def should_send_birthday_voucher(self):
        """Determina si debe enviarse el voucher (7 días antes del cumple)"""
        days = self.days_until_birthday()
        # Enviar 7 días antes si aún no se envió
        return 0 <= days <= 7 and not self.voucher_sent


class CustomerProfile(models.Model):
    """Perfil de cliente para cuentas creadas desde el landing."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        verbose_name='Usuario',
    )
    birth_date = models.DateField('Fecha de nacimiento')
    dni = models.CharField('DNI', max_length=20, blank=True)
    phone = models.CharField('Teléfono', max_length=50, blank=True)
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)

    class Meta:
        verbose_name = 'Perfil de Cliente'
        verbose_name_plural = 'Perfiles de Clientes'
        ordering = ['-created_at']

    def __str__(self):
        email = getattr(self.user, 'email', '')
        return email or str(self.user)


class Service(models.Model):
    """Servicios del camping"""
    title = models.CharField('Título', max_length=200)
    icon = models.ImageField('Icono (imagen)', upload_to='services/icons/', blank=True, null=True)
    icon_fa = models.CharField('Icono FontAwesome', max_length=50, blank=True, default='', help_text='Ej: fa-campground, fa-swimming-pool')
    description = models.TextField('Descripción')
    features = models.JSONField('Características', default=list, help_text='Lista de características del servicio')
    order = models.IntegerField('Orden', default=0)
    is_active = models.BooleanField('Activo', default=True)
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title


class PriceCategory(models.Model):
    """Categorías de precios (Socios, No Socios)"""
    name = models.CharField('Nombre', max_length=100)
    description = models.TextField('Descripción', blank=True)
    is_active = models.BooleanField('Activo', default=True)
    order = models.IntegerField('Orden', default=0)
    
    class Meta:
        verbose_name = 'Categoría de Precio'
        verbose_name_plural = 'Categorías de Precios'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Price(models.Model):
    """Precios de los servicios"""
    category = models.ForeignKey(PriceCategory, on_delete=models.CASCADE, related_name='prices', verbose_name='Categoría')
    item_name = models.CharField('Servicio', max_length=200)
    description = models.TextField('Descripción', blank=True)
    amount = models.DecimalField('Precio', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_free = models.BooleanField('Gratis', default=False)
    order = models.IntegerField('Orden', default=0)
    is_active = models.BooleanField('Activo', default=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)
    
    class Meta:
        verbose_name = 'Precio'
        verbose_name_plural = 'Precios'
        ordering = ['category', 'order', 'item_name']
    
    def __str__(self):
        return f"{self.category.name} - {self.item_name}"


class GalleryImage(models.Model):
    """Imágenes de la galería"""
    title = models.CharField('Título', max_length=200)
    image = models.ImageField('Imagen', upload_to='gallery/')
    description = models.TextField('Descripción', blank=True)
    alt_text = models.CharField('Texto alternativo', max_length=200, help_text='Para SEO')
    order = models.IntegerField('Orden', default=0)
    is_active = models.BooleanField('Activo', default=True)
    uploaded_at = models.DateTimeField('Subida', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Imagen de Galería'
        verbose_name_plural = 'Imágenes de Galería'
        ordering = ['order', '-uploaded_at']
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        image_changed = False
        if self.image:
            if self.pk:
                old = GalleryImage.objects.filter(pk=self.pk).only('image').first()
                image_changed = (old is None) or (old.image != self.image)
            else:
                image_changed = True

        if image_changed and self.image:
            self._normalize_gallery_image()

        super().save(*args, **kwargs)

    def _normalize_gallery_image(self):
        """Normaliza imágenes de galería a 1280x720 si no son verticales.

        - Si la foto es vertical (alto > ancho): se conserva el archivo original.
        - Si es horizontal o cuadrada: se adapta a 1280x720 sin recortar (contain) y se rellenan márgenes.
        """
        try:
            self.image.open('rb')
            with Image.open(self.image) as opened:
                img = ImageOps.exif_transpose(opened)

                width, height = img.size
                # Vertical: no modificar
                if height > width:
                    return

                # Asegurar modo compatible con JPEG
                if img.mode not in ('RGB', 'L'):
                    img = img.convert('RGB')
                elif img.mode == 'L':
                    img = img.convert('RGB')

                target_size = (1280, 720)
                contained = ImageOps.contain(img, target_size, method=Image.LANCZOS)
                needs_upscale = contained.size[0] > width or contained.size[1] > height
                if needs_upscale:
                    contained = contained.filter(ImageFilter.UnsharpMask(radius=1.4, percent=130, threshold=3))

                canvas = Image.new('RGB', target_size, (245, 245, 245))
                offset_x = (target_size[0] - contained.size[0]) // 2
                offset_y = (target_size[1] - contained.size[1]) // 2
                canvas.paste(contained, (offset_x, offset_y))
                fitted = canvas

            buffer = BytesIO()
            fitted.save(
                buffer,
                format='JPEG',
                quality=88,
                optimize=True,
                progressive=True,
                subsampling=0,
            )
            buffer.seek(0)

            base_name = os.path.splitext(os.path.basename(self.image.name))[0] or 'gallery'
            new_name = f"{base_name}_1280x720.jpg"
            self.image.save(new_name, ContentFile(buffer.read()), save=False)
        except Exception:
            # Si falla el procesamiento, se conserva el archivo original
            return


class FAQ(models.Model):
    """Preguntas frecuentes"""
    question = models.CharField('Pregunta', max_length=500)
    answer = models.TextField('Respuesta')
    order = models.IntegerField('Orden', default=0)
    is_active = models.BooleanField('Activo', default=True)
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)
    
    class Meta:
        verbose_name = 'Pregunta Frecuente'
        verbose_name_plural = 'Preguntas Frecuentes'
        ordering = ['order', 'question']
    
    def __str__(self):
        return self.question


class Testimonial(models.Model):
    """Testimonios de clientes"""
    name = models.CharField('Nombre', max_length=200)
    text = models.TextField('Testimonio')
    rating = models.IntegerField('Calificación', default=5, validators=[MinValueValidator(1)])
    photo = models.ImageField('Foto', upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField('Destacado', default=False)
    is_active = models.BooleanField('Activo', default=True)
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Testimonio'
        verbose_name_plural = 'Testimonios'
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.rating}★"


class ContactMessage(models.Model):
    """Mensajes del formulario de contacto"""
    full_name = models.CharField('Nombre completo', max_length=200)
    email = models.EmailField('Email')
    phone = models.CharField('Teléfono', max_length=50)
    message = models.TextField('Mensaje')
    is_read = models.BooleanField('Leído', default=False)
    created_at = models.DateTimeField('Recibido', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Mensaje de Contacto'
        verbose_name_plural = 'Mensajes de Contacto'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.created_at.strftime('%d/%m/%Y')}"


class News(models.Model):
    """Novedades del camping"""
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción')
    image = models.ImageField('Imagen', upload_to='config/news/')
    is_active = models.BooleanField('Activo', default=True)
    order = models.IntegerField('Orden', default=0)
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)
    
    class Meta:
        verbose_name = 'Novedad'
        verbose_name_plural = 'Novedades'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        image_changed = False
        if self.image:
            if self.pk:
                old = News.objects.filter(pk=self.pk).only('image').first()
                image_changed = (old is None) or (old.image != self.image)
            else:
                image_changed = True

        if image_changed and self.image:
            self._normalize_news_cover_image()

        super().save(*args, **kwargs)

    def _normalize_news_cover_image(self):
        """Normaliza la portada de la novedad a 1280x720 si no es vertical.

        - Vertical (alto > ancho): se conserva el archivo original.
        - Horizontal o cuadrada: se adapta a 1280x720 sin recortar (contain) y se rellenan márgenes.
        - Si hay upscale, aplica sharpen leve para mejorar la percepción.
        """
        try:
            self.image.open('rb')
            with Image.open(self.image) as opened:
                img = ImageOps.exif_transpose(opened)

                width, height = img.size
                if height > width:
                    return

                if img.mode not in ('RGB', 'L'):
                    img = img.convert('RGB')
                elif img.mode == 'L':
                    img = img.convert('RGB')

                target_size = (1280, 720)
                contained = ImageOps.contain(img, target_size, method=Image.LANCZOS)
                needs_upscale = contained.size[0] > width or contained.size[1] > height
                if needs_upscale:
                    contained = contained.filter(ImageFilter.UnsharpMask(radius=1.4, percent=130, threshold=3))

                canvas = Image.new('RGB', target_size, (245, 245, 245))
                offset_x = (target_size[0] - contained.size[0]) // 2
                offset_y = (target_size[1] - contained.size[1]) // 2
                canvas.paste(contained, (offset_x, offset_y))
                fitted = canvas

                buffer = BytesIO()
                fitted.save(
                    buffer,
                    format='JPEG',
                    quality=88,
                    optimize=True,
                    progressive=True,
                    subsampling=0,
                )
                buffer.seek(0)

                base_name = os.path.splitext(os.path.basename(self.image.name))[0] or 'news'
                new_name = f"{base_name}_1280x720.jpg"
                self.image.save(new_name, ContentFile(buffer.read()), save=False)
        except Exception:
            return


class NewsImage(models.Model):
    """Imágenes adicionales de una novedad."""

    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Imagen', upload_to='config/news/')
    order = models.IntegerField('Orden', default=0)
    created_at = models.DateTimeField('Creado', auto_now_add=True)

    class Meta:
        verbose_name = 'Imagen de Novedad'
        verbose_name_plural = 'Imágenes de Novedad'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.news.title} (#{self.order})"

    def save(self, *args, **kwargs):
        image_changed = False
        if self.image:
            if self.pk:
                old = NewsImage.objects.filter(pk=self.pk).only('image').first()
                image_changed = (old is None) or (old.image != self.image)
            else:
                image_changed = True

        if image_changed and self.image:
            self._normalize_news_image()

        super().save(*args, **kwargs)

    def _normalize_news_image(self):
        """Normaliza imágenes adicionales a 1280x720 si no son verticales.

        - Vertical (alto > ancho): se conserva el archivo original.
        - Horizontal o cuadrada: se adapta a 1280x720 sin recortar (contain) y se rellenan márgenes.
        - Si hay upscale, aplica sharpen leve.
        """
        try:
            self.image.open('rb')
            with Image.open(self.image) as opened:
                img = ImageOps.exif_transpose(opened)

                width, height = img.size
                if height > width:
                    return

                if img.mode not in ('RGB', 'L'):
                    img = img.convert('RGB')
                elif img.mode == 'L':
                    img = img.convert('RGB')

                target_size = (1280, 720)
                contained = ImageOps.contain(img, target_size, method=Image.LANCZOS)
                needs_upscale = contained.size[0] > width or contained.size[1] > height
                if needs_upscale:
                    contained = contained.filter(ImageFilter.UnsharpMask(radius=1.4, percent=130, threshold=3))

                canvas = Image.new('RGB', target_size, (245, 245, 245))
                offset_x = (target_size[0] - contained.size[0]) // 2
                offset_y = (target_size[1] - contained.size[1]) // 2
                canvas.paste(contained, (offset_x, offset_y))
                fitted = canvas

                buffer = BytesIO()
                fitted.save(
                    buffer,
                    format='JPEG',
                    quality=88,
                    optimize=True,
                    progressive=True,
                    subsampling=0,
                )
                buffer.seek(0)

                base_name = os.path.splitext(os.path.basename(self.image.name))[0] or 'news'
                new_name = f"{base_name}_1280x720.jpg"
                self.image.save(new_name, ContentFile(buffer.read()), save=False)
        except Exception:
            return


class SiteConfiguration(models.Model):
    """Configuración general del sitio"""
    site_name = models.CharField('Nombre del sitio', max_length=200, default='Camping ACA Luján')
    tagline = models.CharField('Eslogan', max_length=500, default='Un lugar para vos')
    hero_image = models.ImageField('Imagen principal', upload_to='config/', blank=True, null=True)
    hero_focus_x = models.IntegerField('Foco horizontal Hero (%)', default=50, validators=[MinValueValidator(0), MaxValueValidator(100)])
    hero_focus_y = models.IntegerField('Foco vertical Hero (%)', default=28, validators=[MinValueValidator(0), MaxValueValidator(100)])
    phone = models.CharField('Teléfono', max_length=50, blank=True)
    email = models.EmailField('Email', blank=True)
    address = models.TextField('Dirección', blank=True)
    instagram_url = models.URLField('Instagram URL', blank=True)
    facebook_url = models.URLField('Facebook URL', blank=True)
    opening_hours = models.TextField('Horarios', default='Miércoles a Lunes de 10 a 18 hs')
    special_alert = models.TextField('Alerta especial', blank=True, help_text='Ej: PILETA CERRADA')
    is_alert_active = models.BooleanField('Mostrar alerta', default=False)
    
    class Meta:
        verbose_name = 'Configuración del Sitio'
        verbose_name_plural = 'Configuración del Sitio'
    
    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        hero_changed = False
        if self.hero_image:
            if self.pk:
                old = SiteConfiguration.objects.filter(pk=self.pk).only('hero_image').first()
                hero_changed = (old is None) or (old.hero_image != self.hero_image)
            else:
                hero_changed = True

        if hero_changed and self.hero_image:
            self._normalize_hero_image()

        super().save(*args, **kwargs)

    def _normalize_hero_image(self):
        """Normaliza la imagen hero a 1920x1080 mostrando imagen completa (contain).

        - Corrige orientación (EXIF)
        - Escala para que entre completa (sin recortar)
        - Rellena márgenes con color suave (blanco)
        - Convierte a JPEG optimizado
        """
        try:
            self.hero_image.open('rb')
            image = Image.open(self.hero_image)
            image = ImageOps.exif_transpose(image)

            # Asegurar modo compatible con JPEG
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')
            elif image.mode == 'L':
                image = image.convert('RGB')

            target_size = (1920, 1080)
            # Contener la imagen completa sin recortar
            original_size = image.size
            contained = ImageOps.contain(image, target_size, method=Image.LANCZOS)

            # Si la imagen original es chica, `contain` hace upscale y puede verse borrosa.
            # No “crea” detalle real, pero un sharpen leve mejora la percepción.
            upscaled = contained.size[0] > original_size[0] or contained.size[1] > original_size[1]
            if upscaled:
                contained = contained.filter(ImageFilter.UnsharpMask(radius=1.6, percent=140, threshold=3))

            # Crear canvas 1920x1080 con fondo blanco suave y centrar la imagen
            canvas = Image.new('RGB', target_size, (245, 245, 245))  # gris muy claro
            offset_x = (target_size[0] - contained.size[0]) // 2
            offset_y = (target_size[1] - contained.size[1]) // 2
            canvas.paste(contained, (offset_x, offset_y))

            image = canvas

            buffer = BytesIO()
            image.save(
                buffer,
                format='JPEG',
                quality=90,
                optimize=True,
                progressive=True,
                subsampling=0,
            )
            buffer.seek(0)

            base_name = os.path.splitext(os.path.basename(self.hero_image.name))[0] or 'hero'
            new_name = f"{base_name}_1920x1080.jpg"

            # Mantener upload_to='config/' (Django lo respeta al guardar en el campo)
            self.hero_image.save(new_name, ContentFile(buffer.read()), save=False)
        except Exception:
            # Si falla el procesamiento, se conserva el archivo original
            return
    
    @classmethod
    def get_config(cls):
        """Obtener la configuración (singleton)"""
        config, created = cls.objects.get_or_create(pk=1)
        return config
