from django.test import TestCase
from djbook.models import Eng


# https://docs.djangoproject.com/en/3.1/topics/testing/advanced/#using-different-testing-frameworks

class TestEng(TestCase):
    """Тестирует класс Eng."""

    def test_str(self):
        eng = Eng()
        eng.id = 100
        eng.word = 'python'
        expected = 'Eng{id:100, word:python}'
        actual = eng.__str__()
        self.assertEqual(expected, actual)
