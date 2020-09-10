from django.test import TestCase
from djbook.models import Rus


# https://docs.djangoproject.com/en/3.1/topics/testing/advanced/#using-different-testing-frameworks

class TestRus(TestCase):
    """Тестирует класс Rus."""

    def test_str(self):
        rus = Rus()
        rus.id = 4
        rus.word = 'артишок'
        expected = 'Rus{id:4, word:артишок}'
        actual = rus.__str__()
        self.assertEqual(expected, actual)
