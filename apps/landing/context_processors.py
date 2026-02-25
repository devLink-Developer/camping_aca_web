from .models import SiteConfiguration, ContactMessage


def site_settings(request):
    """Context processor to make site configuration available in all templates"""
    unread_contact_messages_count = 0

    user = getattr(request, 'user', None)
    session = getattr(request, 'session', {})
    is_staff_admin_mode = bool(
        user
        and getattr(user, 'is_authenticated', False)
        and getattr(user, 'is_staff', False)
        and not session.get('client_mode')
    )

    if is_staff_admin_mode:
        unread_contact_messages_count = ContactMessage.objects.filter(is_read=False).count()

    return {
        'site_config': SiteConfiguration.get_config(),
        'unread_contact_messages_count': unread_contact_messages_count,
    }
