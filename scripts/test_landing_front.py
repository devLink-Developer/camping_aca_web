"""Integration coverage for the public landing's forms and media fallbacks."""

from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.landing.models import ContactMessage, News, NewsImage, SiteConfiguration


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class LandingFrontTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        SiteConfiguration.objects.create(pk=1, hero_focus_x=0, hero_focus_y=0)

    def test_related_image_renders_without_news_cover_in_both_layouts(self):
        # Both odd/even rows have separate template branches. Field paths avoid
        # writing media files or invoking the model's image normalization.
        news_items = News.objects.bulk_create([
            News(title='Primera salida', description='Encuentro al aire libre.', image='', order=0),
            News(title='Segunda salida', description='Encuentro entre arboles.', image='', order=1),
        ])
        related_images = NewsImage.objects.bulk_create([
            NewsImage(news=news_items[0], image='config/news/first-test.jpg'),
            NewsImage(news=news_items[1], image='config/news/second-test.jpg'),
        ])

        response = self.client.get(reverse('landing:home'))

        self.assertEqual(response.status_code, 200)
        for news, image in zip(news_items, related_images):
            with self.subTest(title=news.title):
                self.assertContains(response, news.title)
                self.assertContains(response, f'src="{image.image.url}"', count=1)

    def test_text_only_news_renders_without_image_in_both_layouts(self):
        News.objects.bulk_create([
            News(title='Aviso sin foto uno', description='Informacion de la primera visita.', image='', order=0),
            News(title='Aviso sin foto dos', description='Informacion de la segunda visita.', image='', order=1),
        ])

        response = self.client.get(reverse('landing:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aviso sin foto uno')
        self.assertContains(response, 'Aviso sin foto dos')
        self.assertContains(response, 'Informacion de la primera visita.')
        self.assertContains(response, 'Informacion de la segunda visita.')

    @patch('apps.landing.views.send_mail')
    def test_invalid_contact_preserves_values_and_errors_without_saving(self, send_mail):
        payload = {
            'form_name': 'contact',
            'full_name': 'Ana & familia',
            'email': 'correo-invalido',
            'phone': '11 1234 5678',
            'message': 'Consulta <familia> para el domingo.',
        }
        original_count = ContactMessage.objects.count()

        response = self.client.post(reverse('landing:home'), payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), original_count)
        form = response.context['contact_form']
        self.assertTrue(form.is_bound)
        self.assertIn('email', form.errors)
        for field_name in ('full_name', 'email', 'phone', 'message'):
            with self.subTest(field=field_name):
                self.assertEqual(form[field_name].value(), payload[field_name])
        self.assertContains(response, 'value="Ana &amp; familia"')
        self.assertContains(response, 'value="correo-invalido"')
        self.assertContains(response, 'value="11 1234 5678"')
        self.assertContains(response, 'Consulta &lt;familia&gt; para el domingo.')
        for error in form.errors['email']:
            self.assertContains(response, error)
        send_mail.assert_not_called()
        self.assertEqual(len(mail.outbox), 0)

    def test_zero_hero_focus_is_preserved(self):
        response = self.client.get(reverse('landing:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'object-position: 0% 0%;')
