from django.test import TestCase
from djbook.models import Part


# https://docs.djangoproject.com/en/3.1/topics/testing/advanced/#using-different-testing-frameworks

class TestPart(TestCase):
    """Тестирует класс Part."""

    def test_str(self):
        part = Part()
        part.id = 1
        part.eng_word = 'noun'
        part.rus_word = 'имя существительное'
        expected = 'Part{id:1, eng:noun, rus:имя существительное}'
        actual = part.__str__()
        self.assertEqual(expected, actual)
