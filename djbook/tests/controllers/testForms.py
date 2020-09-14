from django.http import HttpRequest
from django.test import TestCase
from djbook.controllers.forms import get
from djbook.models import Item


# Запуск всех тестов модуля djbook.tests с покрытием:
# coverage run manage.py test djbook.tests

# Запуск тестов класса testForms без покрытия.
# python manage.py test djbook.tests.controllers.testForms


class TestForms(TestCase):
    """Тесты для controllers.forms"""

    def test_display_all_items(self):
        """Тест отображения всех элементов."""

        Item.objects.bulk_create([
            Item(text='test-text-1'),
            Item(text='test-text-2')
        ])
        response = self.client.get('/forms/')
        html = response.content.decode('utf8')
        self.assertIn('test-text-1', html)
        self.assertIn('test-text-2', html)

    def test_get_forms(self):
        """Тестирует get(request). URI: forms/"""

        request = HttpRequest()
        response = get(request)
        # Декодировать двоичный код в utf8-строку.
        html = response.content.decode('utf8')
        self.assertInHTML('<title>Формы</title>', html)

        # Вместо явного создания request и вызова home(request) можно
        # вызвать тестовый клиент Django.
        response = self.client.get('/forms/')
        # Проверить, что использован верный шаблон.
        self.assertTemplateUsed(response, 'djbook/forms.html')

    def test_get_forms_response(self):
        """Тестирует get(request).
        URI: forms-response/?status=ok&message=Foo"""

        response = self.client.get('/forms-response/?status=ok&message=Foo')
        html = response.content.decode('utf8')
        self.assertInHTML('<title>Формы. Ответ.</title>', html)
        self.assertInHTML('<h1>Статус: ok</h1>', html)
        self.assertInHTML('<h3>Сообщение: Foo</h3>', html)
        self.assertTemplateUsed(response, 'djbook/forms-response.html')

    def test_redirect_after_post_success(self):
        """Тестирует post(request). URI: forms/"""

        data = {
            'form-id': 'form-2',  # Скрытое поле с именем формы.
            'text': 'Bar'  # Текстовое поле.
        }
        response = self.client.post('/forms/', data)
        self.assertTrue(response.status_code, 302)
        self.assertTrue('/forms-response/?status=ok&message=Bar', response.url)

    def test_save_item(self):
        """Тест сохранения Item."""
        data = {
            'form-id': 'form-2',  # Скрытое поле с именем формы.
            'text': 'Bar'  # Текстовое поле.
        }
        response = self.client.post('/forms/', data)
        self.assertEqual(Item.objects.count(), 1)
        obj = Item.objects.first()
        self.assertEqual(data['text'], obj.text)
