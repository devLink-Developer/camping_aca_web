"""Integration checks for the isolated local preview database."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_local'

import django
django.setup()

from django.conf import settings
from django.test import Client, TestCase
from scripts.dev_preview import seed_preview


class PreviewIsolationTests(TestCase):
    def test_preview_uses_local_resources(self):
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')
        self.assertNotIn('apps.analytics.middleware.AnalyticsMiddleware', settings.MIDDLEWARE)
        self.assertEqual(os.environ['DEVLINK_DB_HOST'], '127.0.0.1')

    def test_seed_is_repeatable_and_landing_does_not_record_analytics(self):
        from apps.landing.models import Service, Price, GalleryImage, SiteConfiguration
        from apps.analytics.models import PageView, UserSession

        seed_preview()
        first_counts = (Service.objects.count(), GalleryImage.objects.count())
        seed_preview()
        self.assertEqual(first_counts, (Service.objects.count(), GalleryImage.objects.count()))
        self.assertEqual(Price.objects.count(), 0)
        self.assertFalse(SiteConfiguration.get_config().hero_image)
        self.assertTrue(GalleryImage.objects.exists())
        response = Client().get('/', HTTP_HOST='localhost')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PageView.objects.count(), 0)
        self.assertEqual(UserSession.objects.count(), 0)
