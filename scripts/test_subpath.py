"""Deployment contracts for root URLs and a proxy-stripped subpath mount."""

import os
import re
import runpy
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from django.conf import global_settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.test import Client, RequestFactory, TestCase, override_settings
from django.urls import get_script_prefix, set_script_prefix

from apps.analytics.middleware import AnalyticsMiddleware
from apps.analytics.models import PageView, UserSession
from apps.landing.models import ContactMessage, SiteConfiguration


def deployment_settings(prefix, trust_proxy=False):
    environment = {
        'DEBUG': 'true',
        'FORCE_SCRIPT_NAME': prefix,
        'TRUST_PROXY_HEADERS': str(trust_proxy).lower(),
    }
    with patch.dict(os.environ, environment), patch('environ.Env.read_env'):
        # Exercise the actual settings without reading local credentials or
        # loading its production database into Django's active test settings.
        os.environ.pop('SESSION_COOKIE_NAME', None)
        os.environ.pop('CSRF_COOKIE_NAME', None)
        return runpy.run_path(str(Path(__file__).resolve().parents[1] / 'config/settings.py'))


@contextmanager
def mounted(prefix='', trust_proxy=False):
    configured = deployment_settings(prefix, trust_proxy)
    keys = (
        'STATIC_URL', 'MEDIA_URL', 'LOGIN_URL', 'LOGIN_REDIRECT_URL',
        'LOGOUT_REDIRECT_URL', 'SESSION_COOKIE_NAME', 'CSRF_COOKIE_NAME',
        'SESSION_COOKIE_PATH', 'CSRF_COOKIE_PATH', 'SECURE_PROXY_SSL_HEADER',
    )
    values = {key: configured.get(key, getattr(global_settings, key)) for key in keys}
    previous = get_script_prefix()
    try:
        with override_settings(FORCE_SCRIPT_NAME=prefix or None, **values):
            set_script_prefix(prefix or '/')
            yield configured
    finally:
        set_script_prefix(previous)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class SubpathTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        SiteConfiguration.objects.create(pk=1)
        cls.staff = get_user_model().objects.create_user(
            username='mount-review', password='local-test-password',
            email='mount-review@example.test', is_staff=True,
        )

    def test_mount_setting_normalizes_optional_prefix(self):
        for configured, expected in (('', None), ('/', None), ('campingacalujan/', '/campingacalujan')):
            with self.subTest(prefix=configured):
                self.assertEqual(deployment_settings(configured).get('FORCE_SCRIPT_NAME'), expected)

    def test_asset_settings_are_explicit_before_the_first_wsgi_request(self):
        configured = deployment_settings('/campingacalujan')
        self.assertEqual(configured['STATIC_URL'], '/campingacalujan/static/')
        self.assertEqual(configured['MEDIA_URL'], '/campingacalujan/media/')

    def test_landing_assets_forms_and_media_keep_the_mount(self):
        # A lost prefix sends these requests to another application on the host.
        SiteConfiguration.objects.filter(pk=1).update(hero_image='config/hero-test.jpg')
        for prefix in ('', '/campingacalujan'):
            with self.subTest(prefix=prefix), mounted(prefix):
                response = Client().get('/', SCRIPT_NAME=prefix)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(re.search(
                    rf'href="{re.escape(prefix)}/static/css/landing\.css(?:\?[^"]*)?"',
                    response.content.decode(),
                ))
                self.assertContains(response, f'src="{prefix}/media/config/hero-test.jpg"')
                self.assertContains(response, f'action="{prefix}/#contacto"')
                self.assertContains(response, f'action="{prefix}/acceso/"')

    def test_authentication_redirects_remain_inside_the_mount(self):
        for prefix in ('', '/campingacalujan'):
            with self.subTest(prefix=prefix), mounted(prefix):
                client = Client()
                response = client.get('/dashboard/settings/', SCRIPT_NAME=prefix)
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, f'{prefix}/acceso/?next={prefix}/dashboard/settings/')
                response = client.post('/acceso/', {
                    'username': 'mount-review', 'password': 'local-test-password',
                }, SCRIPT_NAME=prefix)
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, f'{prefix}/dashboard/statistics/')
                response = client.get('/salir/', SCRIPT_NAME=prefix)
                self.assertEqual(response.url, f'{prefix}/')

    @override_settings(
        DEBUG=False,
        STATIC_ROOT=Path(__file__).resolve().parents[1] / 'static',
        WHITENOISE_AUTOREFRESH=False,
        WHITENOISE_USE_FINDERS=False,
    )
    def test_static_stylesheet_is_served_after_proxy_strips_the_mount(self):
        # Treat existing source assets as the collected directory so this checks
        # WhiteNoise's production lookup without writing collectstatic output.
        for prefix in ('', '/campingacalujan'):
            with self.subTest(prefix=prefix), mounted(prefix):
                response = Client().get('/static/css/landing.css', SCRIPT_NAME=prefix)
                self.assertEqual(response.status_code, 200)
                self.assertIn('text/css', response['Content-Type'])
                self.assertTrue(b''.join(response.streaming_content))
                response.close()

    def test_contact_post_redirect_and_notification_keep_the_mount(self):
        with mounted('/campingacalujan'):
            response = Client().post('/', {
                'form_name': 'contact', 'full_name': 'Visita en familia',
                'email': 'family@example.test', 'phone': '11 1234 5678',
                'message': 'Consulta para el fin de semana.',
            }, SCRIPT_NAME='/campingacalujan')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/campingacalujan/#contacto')
            self.assertEqual(ContactMessage.objects.count(), 1)
            self.assertEqual(len(mail.outbox), 1)

    def test_client_mode_remembers_admin_page_with_the_mount(self):
        for prefix in ('', '/campingacalujan'):
            with self.subTest(prefix=prefix), mounted(prefix):
                client = Client()
                client.force_login(self.staff)
                response = client.get('/modo-cliente/', {
                    'next': f'{prefix}/dashboard/messages/?status=unread',
                }, SCRIPT_NAME=prefix)
                self.assertEqual(response.url, f'{prefix}/')
                self.assertEqual(client.session['last_admin_path'], f'{prefix}/dashboard/messages/?status=unread')
                response = client.get('/modo-cliente/', {'next': f'{prefix}/'}, SCRIPT_NAME=prefix)
                self.assertEqual(response.url, f'{prefix}/dashboard/messages/?status=unread')

    def test_admin_and_voucher_pages_do_not_create_analytics_under_mount(self):
        middleware = AnalyticsMiddleware(lambda request: HttpResponse('<html>Admin</html>'))
        for internal_path in ('/admin/', '/dashboard/settings/', '/vouchers/'):
            with self.subTest(path=internal_path), mounted('/campingacalujan'):
                request = RequestFactory().get(internal_path, SCRIPT_NAME='/campingacalujan', HTTP_USER_AGENT='Mozilla/5.0')
                request.session = {}
                response = middleware(request)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(PageView.objects.count(), 0)
                self.assertEqual(UserSession.objects.count(), 0)

    def test_malformed_client_mode_next_falls_back_safely(self):
        with mounted('/campingacalujan'):
            client = Client(raise_request_exception=False)
            client.force_login(self.staff)
            response = client.get('/modo-cliente/', {'next': 'https://['}, SCRIPT_NAME='/campingacalujan')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/campingacalujan/')

    def test_chatbot_message_endpoint_keeps_the_mount(self):
        with mounted('/campingacalujan'):
            request = RequestFactory().get('/dashboard/chatbot/clients/', SCRIPT_NAME='/campingacalujan')
            request.user = self.staff
            request.session = {}
            rendered = render_to_string('dashboard/chatbot_clients.html', {}, request=request)
            self.assertIn('/campingacalujan/dashboard/chatbot/clients/__phone__/messages/json/', rendered)

    def test_prefixed_cookies_and_csrf_work_without_root_cookie_names(self):
        # Emulate the sibling application's root cookies being present too.
        with mounted('/campingacalujan'):
            client = Client(enforce_csrf_checks=True)
            client.cookies['sessionid'] = 'another-application-session'
            client.cookies['csrftoken'] = 'another-application-csrf'
            response = client.get('/', SCRIPT_NAME='/campingacalujan')
            csrf_cookie = response.cookies.get('campingaca_csrftoken')
            self.assertIsNotNone(csrf_cookie)
            self.assertEqual(csrf_cookie['path'], '/campingacalujan/')
            token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.content.decode()).group(1)
            # Analytics must use this rendered token, independent of cookie name.
            self.assertContains(response, f"'X-CSRFToken': '{token}'", count=2)
            response = client.post('/acceso/', {
                'username': 'mount-review', 'password': 'local-test-password',
                'csrfmiddlewaretoken': token,
            }, SCRIPT_NAME='/campingacalujan')
            self.assertEqual(response.status_code, 302)
            self.assertIn('campingaca_sessionid', response.cookies)
            self.assertEqual(response.cookies['campingaca_sessionid']['path'], '/campingacalujan/')
            self.assertNotIn('sessionid', response.cookies)

    def test_root_keeps_existing_cookie_names(self):
        with mounted():
            client = Client()
            response = client.get('/')
            self.assertIn('csrftoken', response.cookies)
            self.assertEqual(response.cookies['csrftoken']['path'], '/')
            response = client.post('/acceso/', {
                'username': 'mount-review', 'password': 'local-test-password',
            })
            self.assertIn('sessionid', response.cookies)
            self.assertEqual(response.cookies['sessionid']['path'], '/')

    def test_trusted_proxy_https_is_opt_in(self):
        for trusted, expected_scheme in ((False, 'http'), (True, 'https')):
            with self.subTest(trusted=trusted), mounted('/campingacalujan', trust_proxy=trusted):
                request = RequestFactory().get('/cuenta/recuperar/', SCRIPT_NAME='/campingacalujan',
                                               HTTP_HOST='testserver', HTTP_X_FORWARDED_PROTO='https')
                self.assertEqual(request.build_absolute_uri('/campingacalujan/cuenta/recuperar/'),
                                 f'{expected_scheme}://testserver/campingacalujan/cuenta/recuperar/')

    def test_reset_email_uses_public_https_mount_behind_trusted_proxy(self):
        with mounted('/campingacalujan', trust_proxy=True):
            response = Client().post('/cuenta/recuperar/', {
                'email': 'mount-review@example.test',
            }, SCRIPT_NAME='/campingacalujan', HTTP_HOST='testserver', HTTP_X_FORWARDED_PROTO='https')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/campingacalujan/cuenta/recuperar/enviado/')
            self.assertEqual(len(mail.outbox), 1)
            self.assertIn('https://testserver/campingacalujan/cuenta/restablecer/', mail.outbox[0].body)
