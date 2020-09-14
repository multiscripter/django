from django.test import TestCase
from djbook.models.item import Item


# Запуск тестов класса TestItem без покрытия.
# python manage.py test djbook.tests.models.testItem


class TestItem(TestCase):
    """Тестирует класс Item."""

    def test_saving_and_retrieving_items(self):
        """Тест сохранения и получения элементов."""

        expected = {
            'text': 'Текст первого элемента'
        }
        obj = Item()
        obj.text = expected['text']
        obj.save()

        saved = Item.objects.all()
        self.assertEqual(expected['text'], saved[0].text)
