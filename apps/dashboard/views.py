from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Max
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
from datetime import datetime

from django.utils.dateparse import parse_date

from PIL import Image, UnidentifiedImageError

from apps.landing.models import (
    Service,
    Price,
    PriceCategory,
    GalleryImage,
    FAQ,
    Testimonial,
    ContactMessage,
    SiteConfiguration,
    News,
    NewsImage,
    Lead,
    CustomerProfile,
)
from apps.vouchers.models import Voucher
from apps.analytics.models import PageView, UserSession

from .devlink_db import connect_devlink, fetch_one, fetch_all, execute

staff_required = user_passes_test(lambda u: u.is_active and u.is_staff, login_url=settings.LOGIN_URL)


def _now_ms() -> int:
    return int(datetime.utcnow().timestamp() * 1000)


@staff_required
def dashboard_home(request):
    """Dashboard principal con resumen"""
    return redirect('dashboard:statistics')

    # Estadísticas rápidas
    today = timezone.now().date()
    week_ago = timezone.now() - timedelta(days=7)
    
    stats = {
        'total_services': Service.objects.filter(is_active=True).count(),
        'total_gallery_images': GalleryImage.objects.filter(is_active=True).count(),
        'total_testimonials': Testimonial.objects.filter(is_active=True).count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'active_vouchers': Voucher.objects.filter(status='active').count(),
        'used_vouchers_today': Voucher.objects.filter(
            used_date__date=today
        ).count(),
        'page_views_week': PageView.objects.filter(timestamp__gte=week_ago).count(),
        'sessions_week': UserSession.objects.filter(start_time__gte=week_ago).count(),
    }
    
    # Mensajes recientes
    recent_messages = ContactMessage.objects.all()[:5]
    
    # Vouchers recientes
    recent_vouchers = Voucher.objects.all()[:5]
    
    context = {
        'stats': stats,
        'recent_messages': recent_messages,
        'recent_vouchers': recent_vouchers,
    }
    
    return render(request, 'dashboard/home.html', context)


@staff_required
def dashboard_messages(request):
    """Lista de mensajes de contacto"""
    status = request.GET.get('status', 'all')
    qs = ContactMessage.objects.all()

    if status == 'unread':
        qs = qs.filter(is_read=False)
    elif status == 'read':
        qs = qs.filter(is_read=True)

    qs = qs.order_by('-created_at')
    paginator = Paginator(qs, 25)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    # Marcar como leído si se especifica
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        if message_id:
            msg = get_object_or_404(ContactMessage, id=message_id)
            msg.is_read = True
            msg.save(update_fields=['is_read'])
            messages.success(request, 'Mensaje marcado como leído.')
            redirect_url = request.POST.get('redirect') or request.get_full_path()
            return redirect(redirect_url)
    
    context = {
        'contact_messages': page_obj.object_list,
        'page_obj': page_obj,
        'status': status,
        'total_messages': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
    }
    
    return render(request, 'dashboard/messages.html', context)


@staff_required
def dashboard_statistics(request):
    """Página de estadísticas con el estilo de la web"""
    today = timezone.now().date()
    week_ago = timezone.now() - timedelta(days=7)
    month_ago = timezone.now() - timedelta(days=30)
    
    # Métricas principales (enfocadas para el cliente)
    visits_week = PageView.objects.filter(timestamp__gte=week_ago).values('session_id').distinct().count()
    registered_users_week = CustomerProfile.objects.filter(created_at__gte=week_ago).count()
    campaign_leads_week = Lead.objects.filter(created_at__gte=week_ago).count()

    stats = {
        # Tráfico
        'total_visits': PageView.objects.values('session_id').distinct().count(),
        'visits_today': PageView.objects.filter(timestamp__date=today).values('session_id').distinct().count(),
        'visits_week': visits_week,
        'visits_month': PageView.objects.filter(timestamp__gte=month_ago).values('session_id').distinct().count(),

        # Clientes registrados (cuentas creadas desde el landing)
        'total_registered_users': CustomerProfile.objects.count(),
        'registered_users_week': registered_users_week,

        # Registros campaña (formulario /campaing/)
        'total_campaign_leads': Lead.objects.count(),
        'campaign_leads_week': campaign_leads_week,

        # Consultas
        'total_messages': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'messages_week': ContactMessage.objects.filter(created_at__gte=week_ago).count(),
    }

    # Conversión (semanal)
    if visits_week:
        stats['conversion_registered_users_week'] = round((registered_users_week / visits_week) * 100, 1)
        stats['conversion_campaign_leads_week'] = round((campaign_leads_week / visits_week) * 100, 1)
    else:
        stats['conversion_registered_users_week'] = 0.0
        stats['conversion_campaign_leads_week'] = 0.0
    
    # Páginas más visitadas (últimos 30 días)
    top_pages = PageView.objects.filter(
        timestamp__gte=month_ago
    ).values('path').annotate(
        visits=Count('session_id', distinct=True)
    ).order_by('-visits')[:10]
    
    # Visitas por día (últimos 7 días)
    daily_visits = []
    for i in range(7):
        date = today - timedelta(days=6 - i)
        count = PageView.objects.filter(timestamp__date=date).values('session_id').distinct().count()
        daily_visits.append({'date': date.strftime('%d/%m'), 'visits': count})
    
    context = {
        'stats': stats,
        'top_pages': top_pages,
        'daily_visits': json.dumps(daily_visits),
    }
    
    return render(request, 'dashboard/statistics.html', context)


@staff_required
def dashboard_settings(request):
    """Página de configuración del sitio con el estilo de la web"""
    site_config, created = SiteConfiguration.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        # Actualizar configuración
        site_config.site_name = request.POST.get('site_name', site_config.site_name)
        site_config.tagline = request.POST.get('tagline', site_config.tagline)
        site_config.phone = request.POST.get('phone', site_config.phone)
        site_config.email = request.POST.get('email', site_config.email)
        site_config.address = request.POST.get('address', site_config.address)
        site_config.opening_hours = request.POST.get('opening_hours', site_config.opening_hours)
        site_config.instagram_url = request.POST.get('instagram_url', site_config.instagram_url)
        site_config.facebook_url = request.POST.get('facebook_url', site_config.facebook_url)
        site_config.special_alert = request.POST.get('special_alert', site_config.special_alert)
        site_config.is_alert_active = request.POST.get('is_alert_active') == 'on'
        
        # Manejar imagen hero si se sube
        if 'hero_image' in request.FILES:
            hero_file = request.FILES['hero_image']

            # Validación: evitar que una imagen chica se vea pixelada/borrosa.
            # Como el hero se normaliza a 1920x1080 y se muestra con `background-size: contain`,
            # si el archivo requiere *upscale* no hay forma de “mejorar” calidad.
            try:
                hero_file.seek(0)
                with Image.open(hero_file) as img:
                    width, height = img.size
            except (UnidentifiedImageError, OSError):
                messages.error(request, '❌ La imagen Hero no parece ser un archivo de imagen válido.')
                return redirect('dashboard:settings')
            finally:
                try:
                    hero_file.seek(0)
                except Exception:
                    pass

            target_w, target_h = 1920, 1080
            needs_upscale = (width < target_w) and (height < target_h)
            if needs_upscale:
                messages.warning(
                    request,
                    f'⚠️ La imagen Hero es de {width}x{height}px. Se va a mostrar, pero puede verse borrosa en pantallas grandes. Recomendado: {target_w}x{target_h}px (o al menos {target_w}px de ancho o {target_h}px de alto).'
                )

            site_config.hero_image = hero_file
        
        site_config.save()
        messages.success(request, '✅ Configuración actualizada correctamente')
        return redirect('dashboard:settings')
    
    context = {
        'site_config': site_config,
    }
    
    return render(request, 'dashboard/settings.html', context)


@staff_required
def manage_services(request):
    """Gestión de servicios"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            features_raw = request.POST.get('features', '')
            features = [f.strip() for f in features_raw.splitlines() if f.strip()]
            icon_file = request.FILES.get('icon') or None
            icon_fa = '' if icon_file else (request.POST.get('icon_fa', '') or '')
            Service.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                icon=icon_file,
                icon_fa=icon_fa,
                features=features,
                order=int(request.POST.get('order', 0) or 0),
                is_active=True
            )
            messages.success(request, '✅ Servicio creado exitosamente')
        
        elif action == 'update':
            service_id = request.POST.get('service_id')
            service = Service.objects.get(id=service_id)
            service.title = request.POST.get('title')
            service.description = request.POST.get('description')
            if 'icon' in request.FILES:
                # Nueva imagen sube: borra icono FA
                service.icon = request.FILES['icon']
                service.icon_fa = ''
            else:
                icon_fa = request.POST.get('icon_fa', '') or ''
                if icon_fa:
                    # Icono FA seleccionado: borra imagen
                    service.icon_fa = icon_fa
                    if service.icon:
                        service.icon.delete(save=False)
                        service.icon = None
            features_raw = request.POST.get('features', '')
            service.features = [f.strip() for f in features_raw.splitlines() if f.strip()]
            service.order = int(request.POST.get('order', service.order) or service.order)
            service.save()
            messages.success(request, '✅ Servicio actualizado exitosamente')
        
        elif action == 'delete':
            service_id = request.POST.get('service_id')
            Service.objects.filter(id=service_id).delete()
            messages.success(request, '✅ Servicio eliminado')
        
        elif action == 'toggle':
            service_id = request.POST.get('service_id')
            service = Service.objects.get(id=service_id)
            service.is_active = not service.is_active
            service.save()
            messages.success(request, '✅ Estado del servicio actualizado')
        
        return redirect('dashboard:manage_services')
    
    services = Service.objects.all().order_by('-created_at')
    
    context = {
        'services': services,
    }
    
    return render(request, 'dashboard/manage_services.html', context)


@staff_required
def manage_gallery(request):
    """Gestión de galería"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'upload':
            if 'image' in request.FILES:
                title = request.POST.get('title', 'Imagen de galería')
                description = request.POST.get('description', '')
                GalleryImage.objects.create(
                    image=request.FILES['image'],
                    title=title,
                    description=description,
                    alt_text=title,
                    is_active=True
                )
                messages.success(request, '✅ Imagen subida exitosamente')
        
        elif action == 'delete':
            image_id = request.POST.get('image_id')
            GalleryImage.objects.filter(id=image_id).delete()
            messages.success(request, '✅ Imagen eliminada')
        
        elif action == 'toggle':
            image_id = request.POST.get('image_id')
            image = GalleryImage.objects.get(id=image_id)
            image.is_active = not image.is_active
            image.save()
            messages.success(request, '✅ Estado de la imagen actualizado')
        
        return redirect('dashboard:manage_gallery')
    
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    
    context = {
        'images': images,
    }
    
    return render(request, 'dashboard/manage_gallery.html', context)


@staff_required
def manage_prices(request):
    """Gestión de precios"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            category_id = request.POST.get('category_id')
            if category_id:
                category = PriceCategory.objects.get(id=category_id)
                Price.objects.create(
                    category=category,
                    item_name=request.POST.get('item_name'),
                    description=request.POST.get('description', ''),
                    amount=request.POST.get('amount'),
                    is_active=True
                )
                messages.success(request, '✅ Precio creado exitosamente')
            else:
                messages.error(request, '❌ Debes seleccionar una categoría')
        
        elif action == 'delete':
            price_id = request.POST.get('price_id')
            Price.objects.filter(id=price_id).delete()
            messages.success(request, '✅ Precio eliminado')
        
        elif action == 'toggle':
            price_id = request.POST.get('price_id')
            price = Price.objects.get(id=price_id)
            price.is_active = not price.is_active
            price.save()
            messages.success(request, '✅ Estado del precio actualizado')
        
        return redirect('dashboard:manage_prices')
    
    prices = Price.objects.all().order_by('category', 'amount')
    categories = PriceCategory.objects.filter(is_active=True)
    
    context = {
        'prices': prices,
        'categories': categories,
    }
    
    return render(request, 'dashboard/manage_prices.html', context)


@staff_required
def manage_faqs(request):
    """Gestión de preguntas frecuentes"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            FAQ.objects.create(
                question=request.POST.get('question'),
                answer=request.POST.get('answer'),
                is_active=True
            )
            messages.success(request, '✅ Pregunta frecuente creada exitosamente')
        
        elif action == 'delete':
            faq_id = request.POST.get('faq_id')
            FAQ.objects.filter(id=faq_id).delete()
            messages.success(request, '✅ Pregunta eliminada')
        
        elif action == 'toggle':
            faq_id = request.POST.get('faq_id')
            faq = FAQ.objects.get(id=faq_id)
            faq.is_active = not faq.is_active
            faq.save()
            messages.success(request, '✅ Estado de la pregunta actualizado')
        
        return redirect('dashboard:manage_faqs')
    
    faqs = FAQ.objects.all().order_by('-created_at')
    
    context = {
        'faqs': faqs,
    }
    
    return render(request, 'dashboard/manage_faqs.html', context)


@staff_required
def manage_news(request):
    """Gestión de novedades"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            uploaded_images = request.FILES.getlist('images')
            if not uploaded_images and 'image' in request.FILES:
                uploaded_images = [request.FILES['image']]

            if uploaded_images:
                raw_order = request.POST.get('order', 0)
                try:
                    order_value = int(raw_order) if str(raw_order).strip() != '' else 0
                except (TypeError, ValueError):
                    order_value = 0

                news = News.objects.create(
                    title=request.POST.get('title'),
                    description=request.POST.get('description'),
                    image=uploaded_images[0],
                    order=order_value,
                    is_active=(request.POST.get('is_active') == 'on'),
                )

                for index, img in enumerate(uploaded_images):
                    NewsImage.objects.create(news=news, image=img, order=index)

                messages.success(request, '✅ Novedad creada exitosamente')
            else:
                messages.error(request, '❌ Debe incluir una imagen')
        
        elif action == 'delete':
            news_id = request.POST.get('news_id')
            News.objects.filter(id=news_id).delete()
            messages.success(request, '✅ Novedad eliminada')
        
        elif action == 'toggle':
            news_id = request.POST.get('news_id')
            news = News.objects.get(id=news_id)
            news.is_active = not news.is_active
            news.save()
            messages.success(request, '✅ Estado de la novedad actualizado')
        
        elif action == 'update':
            news_id = request.POST.get('news_id')
            news = News.objects.get(id=news_id)
            news.title = request.POST.get('title')
            news.description = request.POST.get('description')
            news.order = request.POST.get('order', news.order)
            if 'image' in request.FILES:
                news.image = request.FILES['image']
                NewsImage.objects.get_or_create(news=news, image=news.image, defaults={'order': 0})

            extra_images = request.FILES.getlist('images')
            if extra_images:
                max_order = NewsImage.objects.filter(news=news).aggregate(Max('order')).get('order__max')
                next_order = (max_order or 0) + 1
                for offset, img in enumerate(extra_images):
                    NewsImage.objects.create(news=news, image=img, order=next_order + offset)
            news.save()
            messages.success(request, '✅ Novedad actualizada exitosamente')

        elif action == 'delete_image':
            image_id = request.POST.get('news_image_id')
            if image_id:
                NewsImage.objects.filter(id=image_id).delete()
                messages.success(request, '✅ Imagen eliminada')
        
        return redirect('dashboard:manage_news')
    
    news_list = News.objects.all().prefetch_related('images').order_by('order', '-created_at')
    next_order = (News.objects.aggregate(Max('order')).get('order__max') or 0) + 1
    
    context = {
        'news_list': news_list,
        'next_order': next_order,
    }
    
    return render(request, 'dashboard/manage_news.html', context)


_DIRECCION_LABELS = {"in": "Entrante (usuario)", "out": "Saliente (bot)"}
_TIPO_LABELS = {
    "text": "Texto",
    "interactive": "Interactivo",
    "image": "Imagen",
    "audio": "Audio",
    "video": "Video",
    "document": "Documento",
    "location": "Ubicación",
    "template": "Plantilla",
}


@staff_required
def chatbot_statistics(request):
    """Estadísticas del chatbot (Devlink DB)."""

    used_port = None
    devlink_error = None
    total_clients = active_clients = 0
    total_messages = messages_7d = messages_30d = 0
    open_sessions = total_sessions = 0
    last_message_at = None
    by_direction = []
    by_type = []
    daily_labels = []
    daily_in = []
    daily_out = []

    try:
        conn, used_port = connect_devlink(readonly=True)
        try:
            # ── Clientes (1 query en vez de 2) ────────────────────────────
            row_c = fetch_one(
                conn,
                """
                SELECT COUNT(*),
                       COUNT(*) FILTER (WHERE activo = true)
                FROM public.clientes;
                """,
            ) or [0, 0]
            total_clients, active_clients = row_c[0], row_c[1]

            # ── Mensajes ───────────────────────────────────────────────────
            row = fetch_one(
                conn,
                """
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '7 days')  AS last_7d,
                    COUNT(*) FILTER (WHERE created_at >= NOW() - INTERVAL '30 days') AS last_30d,
                    MAX(created_at AT TIME ZONE 'America/Argentina/Buenos_Aires')     AS last_at
                FROM public.mensajes;
                """,
            )
            if row:
                total_messages, messages_7d, messages_30d, last_message_at = row

            # ── Sesiones (1 query en vez de 2) ─────────────────────────────
            row_s = fetch_one(
                conn,
                """
                SELECT COUNT(*),
                       COUNT(*) FILTER (WHERE activa = true)
                FROM public.sesiones;
                """,
            ) or [0, 0]
            total_sessions, open_sessions = row_s[0], row_s[1]

            # ── Desglose por dirección (todo el tiempo) ────────────────────
            raw_dir = fetch_all(
                conn,
                """
                SELECT direccion, COUNT(*) AS cnt
                FROM public.mensajes
                GROUP BY direccion
                ORDER BY cnt DESC;
                """,
            )
            by_direction = [
                (_DIRECCION_LABELS.get(r[0], r[0].capitalize()), r[1])
                for r in raw_dir
            ]

            # ── Desglose por tipo (todo el tiempo) ────────────────────────
            raw_type = fetch_all(
                conn,
                """
                SELECT tipo, COUNT(*) AS cnt
                FROM public.mensajes
                GROUP BY tipo
                ORDER BY cnt DESC;
                """,
            )
            by_type = [
                (_TIPO_LABELS.get(r[0], r[0].capitalize()), r[1])
                for r in raw_type
            ]

            # ── Actividad diaria (últimos 30 días) ────────────────────────
            daily_rows = fetch_all(
                conn,
                """
                SELECT
                    (created_at AT TIME ZONE 'America/Argentina/Buenos_Aires')::date AS dia,
                    SUM(CASE WHEN direccion = 'in'  THEN 1 ELSE 0 END) AS entrantes,
                    SUM(CASE WHEN direccion = 'out' THEN 1 ELSE 0 END) AS salientes
                FROM public.mensajes
                WHERE created_at >= NOW() - INTERVAL '30 days'
                GROUP BY 1
                ORDER BY 1;
                """,
            )
            for dr in daily_rows:
                daily_labels.append(str(dr[0]))   # 'YYYY-MM-DD'
                daily_in.append(int(dr[1] or 0))
                daily_out.append(int(dr[2] or 0))

        finally:
            conn.close()
    except Exception as exc:  # noqa: BLE001
        devlink_error = f"No se pudo leer la DB Devlink: {exc}"

    context = {
        "db_port_used": used_port,
        "devlink_error": devlink_error,
        "last_message_at": last_message_at,
        "stats": {
            "total_clients": total_clients,
            "active_clients": active_clients,
            "total_messages": total_messages,
            "messages_7d": messages_7d,
            "messages_30d": messages_30d,
            "open_sessions": open_sessions,
            "total_sessions": total_sessions,
        },
        "by_direction": by_direction,
        "by_type": by_type,
        "daily_labels": json.dumps(daily_labels),
        "daily_in": json.dumps(daily_in),
        "daily_out": json.dumps(daily_out),
    }
    return render(request, "dashboard/chatbot_statistics.html", context)


@staff_required
def chatbot_clients(request):
    """Clientes del chatbot (listado + alta) en Devlink DB."""

    query = (request.GET.get("q") or "").strip()
    page = int(request.GET.get("page", "1") or 1)
    page_size = 25
    offset = (page - 1) * page_size

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            phone_number = (request.POST.get("phone_number") or "").strip()
            nombre = (request.POST.get("nombre") or "").strip() or None
            correo = (request.POST.get("correo") or "").strip() or None
            direccion = (request.POST.get("direccion") or "").strip() or None
            alias_waba = (request.POST.get("alias_waba") or "").strip() or None
            fecha_nacimiento_raw = (request.POST.get("fecha_nacimiento") or "").strip() or None
            marketing_opt_in = request.POST.get("marketing_opt_in") == "on"
            activo = request.POST.get("activo") == "on"

            if not phone_number:
                messages.error(request, "❌ El teléfono es obligatorio")
                return redirect("dashboard:chatbot_clients")

            fecha_nacimiento = parse_date(fecha_nacimiento_raw) if fecha_nacimiento_raw else None

            now_ms = _now_ms()
            try:
                conn, _ = connect_devlink(readonly=False)
                try:
                    execute(
                        conn,
                        """
                        INSERT INTO public.clientes (
                            phone_number,
                            nombre,
                            primer_contacto_ms,
                            ultimo_contacto_ms,
                            mensajes_totales,
                            ultimo_mensaje,
                            activo,
                            created_at,
                            updated_at,
                            alias_waba,
                            correo,
                            direccion,
                            fecha_nacimiento,
                            marketing_opt_in
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s, %s, %s, %s, %s
                        );
                        """,
                        (
                            phone_number,
                            nombre,
                            now_ms,
                            now_ms,
                            0,
                            None,
                            activo,
                            alias_waba,
                            correo,
                            direccion,
                            fecha_nacimiento,
                            marketing_opt_in,
                        ),
                    )
                    messages.success(request, "✅ Cliente creado")
                finally:
                    conn.close()
            except Exception as exc:  # noqa: BLE001
                msg = str(exc)
                if "clientes_pkey" in msg or "duplicate key" in msg.lower():
                    messages.error(request, "❌ Ya existe un cliente con ese teléfono")
                else:
                    messages.error(request, "❌ No se pudo crear el cliente")

            return redirect("dashboard:chatbot_clients")

    activo_filter = (request.GET.get("activo_filter") or "").strip()  # "1"=activos, "0"=inactivos, ""=todos

    used_port = None
    devlink_error = None
    total = 0
    rows = []
    summary = {"total": 0, "active": 0, "marketing": 0}

    try:
        conn, used_port = connect_devlink(readonly=True)
        try:
            # ── 1 sola query: summary global + lista paginada via CTE ──────
            cte_params: list = []
            conditions = []
            if query:
                conditions.append("(phone_number ILIKE %s OR COALESCE(nombre, '') ILIKE %s)")
                cte_params.extend([f"%{query}%", f"%{query}%"])
            if activo_filter == "1":
                conditions.append("activo = true")
            elif activo_filter == "0":
                conditions.append("activo = false")

            where_sql = ("WHERE " + " AND ".join(conditions)) if conditions else ""
            cte_params.extend([page_size, offset])

            raw_rows = fetch_all(
                conn,
                f"""
                WITH summary AS (
                    SELECT
                        COUNT(*)                                          AS total,
                        COUNT(*) FILTER (WHERE activo = true)             AS active,
                        COUNT(*) FILTER (WHERE marketing_opt_in = true)   AS marketing
                    FROM public.clientes
                ),
                paged AS (
                    SELECT
                        phone_number,
                        nombre,
                        correo,
                        activo,
                        mensajes_totales,
                        created_at,
                        updated_at,
                        alias_waba,
                        marketing_opt_in,
                        CASE WHEN primer_contacto_ms > 0
                             THEN to_timestamp(primer_contacto_ms / 1000.0)
                        END                     AS primer_contacto,
                        COUNT(*) OVER()         AS filtered_count
                    FROM public.clientes
                    {where_sql}
                    ORDER BY updated_at DESC NULLS LAST
                    LIMIT %s OFFSET %s
                )
                SELECT p.*, s.total, s.active, s.marketing
                FROM paged p
                CROSS JOIN summary s;
                """,
                cte_params,
            )

            if raw_rows:
                total   = raw_rows[0][10]   # filtered_count
                summary = {
                    "total":     raw_rows[0][11] or 0,
                    "active":    raw_rows[0][12] or 0,
                    "marketing": raw_rows[0][13] or 0,
                }
                rows = [r[:10] for r in raw_rows]
            else:
                # No rows returned — still need summary totals
                s = fetch_one(
                    conn,
                    """
                    SELECT COUNT(*),
                           COUNT(*) FILTER (WHERE activo = true),
                           COUNT(*) FILTER (WHERE marketing_opt_in = true)
                    FROM public.clientes;
                    """,
                ) or [0, 0, 0]
                summary = {"total": s[0] or 0, "active": s[1] or 0, "marketing": s[2] or 0}
                total = 0
        finally:
            conn.close()
    except Exception:
        devlink_error = "No se pudo leer la DB Devlink (conexión o tablas)."

    total_pages = max(1, (int(total) + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))

    # Sliding window: up to 7 pages around current
    half = 3
    start_p = max(1, page - half)
    end_p = min(total_pages, page + half)
    if end_p - start_p < 6:
        start_p = max(1, end_p - 6)
        end_p = min(total_pages, start_p + 6)
    clients_page_range = list(range(start_p, end_p + 1))

    context = {
        "db_port_used": used_port,
        "devlink_error": devlink_error,
        "q": query,
        "activo_filter": activo_filter,
        "clients": rows,
        "summary": summary,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": int(total),
            "total_pages": total_pages,
            "has_prev": page > 1,
            "has_next": page < total_pages,
            "prev_page": page - 1,
            "next_page": page + 1,
            "page_range": clients_page_range,
        },
    }
    return render(request, "dashboard/chatbot_clients.html", context)


@staff_required
def chatbot_client_messages(request, phone: str):
    """Mensajes de un cliente del chatbot (entrantes y respuestas del bot) — página completa."""
    page = int(request.GET.get("page", "1") or 1)
    page_size = 40
    offset = (page - 1) * page_size

    used_port = None
    devlink_error = None
    client = None
    messages_rows = []
    total = 0

    try:
        conn, used_port = connect_devlink(readonly=True)
        try:
            client = fetch_one(
                conn,
                """
                SELECT phone_number, nombre, alias_waba, correo, activo,
                       mensajes_totales, updated_at
                FROM public.clientes
                WHERE phone_number = %s;
                """,
                [phone],
            )

            # direccion='in' = cliente, direccion='out' = bot
            raw = fetch_all(
                conn,
                """
                SELECT id,
                       direccion,
                       contenido,
                       to_timestamp(timestamp_ms / 1000.0) AT TIME ZONE 'America/Argentina/Buenos_Aires' AS ts,
                       delivery_status,
                       COUNT(*) OVER() AS total_count
                FROM public.mensajes
                WHERE phone_number = %s
                  AND direccion IN ('in', 'out')
                ORDER BY timestamp_ms DESC
                LIMIT %s OFFSET %s;
                """,
                [phone, page_size, offset],
            )
            total = raw[0][5] if raw else 0
            messages_rows = [r[:5] for r in raw]
        finally:
            conn.close()
    except Exception:
        devlink_error = "No se pudo leer la DB Devlink (conexión o tablas)."

    total_pages = max(1, (int(total) + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))

    # Sliding window: up to 7 pages around current
    half = 3
    start_p = max(1, page - half)
    end_p = min(total_pages, page + half)
    if end_p - start_p < 6:
        start_p = max(1, end_p - 6)
        end_p = min(total_pages, start_p + 6)
    msg_page_range = list(range(start_p, end_p + 1))

    context = {
        "phone": phone,
        "client": client,
        "messages_rows": messages_rows,
        "devlink_error": devlink_error,
        "db_port_used": used_port,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": int(total),
            "total_pages": total_pages,
            "has_prev": page > 1,
            "has_next": page < total_pages,
            "prev_page": page - 1,
            "next_page": page + 1,
            "page_range": msg_page_range,
        },
    }
    return render(request, "dashboard/chatbot_client_messages.html", context)


@staff_required
def chatbot_client_messages_json(request, phone: str):
    """Endpoint JSON para cargar mensajes de un cliente en un modal (AJAX)."""
    page = int(request.GET.get("page", "1") or 1)
    page_size = 50
    offset = (page - 1) * page_size

    try:
        conn, _ = connect_devlink(readonly=True)
        try:
            client_row = fetch_one(
                conn,
                "SELECT phone_number, nombre, alias_waba, mensajes_totales FROM public.clientes WHERE phone_number = %s;",
                [phone],
            )
            raw = fetch_all(
                conn,
                """
                SELECT id,
                       direccion,
                       contenido,
                       to_char(
                           to_timestamp(timestamp_ms / 1000.0) AT TIME ZONE 'America/Argentina/Buenos_Aires',
                           'DD/MM/YYYY HH24:MI'
                       ) AS ts,
                       delivery_status,
                       COUNT(*) OVER() AS total_count
                FROM public.mensajes
                WHERE phone_number = %s
                  AND direccion IN ('in', 'out')
                ORDER BY timestamp_ms DESC
                LIMIT %s OFFSET %s;
                """,
                [phone, page_size, offset],
            )
        finally:
            conn.close()
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=500)

    total = raw[0][5] if raw else 0
    total_pages = max(1, (int(total) + page_size - 1) // page_size)

    return JsonResponse({
        "phone": phone,
        "client_name": client_row[1] if client_row else None,
        "client_alias": client_row[2] if client_row else None,
        "total": int(total),
        "page": page,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "messages": [
            {
                "id": r[0],
                "direccion": r[1],
                "contenido": r[2] or "",
                "ts": r[3] or "",
                "delivery_status": r[4] or "",
            }
            for r in raw
        ],
    })
