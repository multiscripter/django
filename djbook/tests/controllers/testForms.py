from django.http import HttpRequest
from django.test import TestCase
from djbook.controllers.forms import get


class TestForms(TestCase):
    """Тесты для controllers.forms"""

    def test_get_forms(self):
        """Тестирует get(request). URI: forms/"""

        request = HttpRequest()
        response = get(request)
        # Декодировать двоичный код в utf8-строку.
        html = response.content.decode('utf8')
        self.assertInHTML('<title>Формы</title>', html)

        # Весто явного создания request и вызова home(request) можно
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

    def test_post(self):
        """Тестирует post(request). URI: forms/"""
        # TODO: дописать тест с методом POST.
