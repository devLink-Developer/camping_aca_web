"""Public media must stay inside MEDIA_ROOT, including encoded paths and links."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import SkipTest

from django.test import SimpleTestCase, override_settings


class MediaSecurityTests(SimpleTestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.media = self.root / 'media'
        self.media.mkdir()
        (self.media / 'photo.txt').write_text('public media', encoding='utf-8')
        (self.root / 'outside.txt').write_text('private test fixture', encoding='utf-8')
        self.settings_override = override_settings(MEDIA_ROOT=self.media)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)

    def test_existing_file_is_served(self):
        response = self.client.get('/media/photo.txt')
        self.addCleanup(response.close)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b''.join(response.streaming_content), b'public media')

    def test_encoded_parent_traversal_returns_404(self):
        for path in ('/media/%2e%2e/outside.txt', '/media/../outside.txt', '/media/%252e%252e/outside.txt'):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.addCleanup(response.close)
                self.assertEqual(response.status_code, 404)

    def test_missing_file_and_directory_return_404(self):
        for path in ('/media/missing.txt', '/media/'):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 404)

    def test_symlink_to_file_outside_media_returns_404(self):
        try:
            (self.media / 'link.txt').symlink_to(self.root / 'outside.txt')
        except (OSError, NotImplementedError) as error:
            raise SkipTest('Creating symlinks is unavailable on this machine.') from error
        self.assertEqual(self.client.get('/media/link.txt').status_code, 404)

    def test_symlink_to_directory_outside_media_returns_404(self):
        try:
            (self.media / 'linked-directory').symlink_to(self.root, target_is_directory=True)
        except (OSError, NotImplementedError) as error:
            raise SkipTest('Creating symlinks is unavailable on this machine.') from error
        self.assertEqual(self.client.get('/media/linked-directory/outside.txt').status_code, 404)
