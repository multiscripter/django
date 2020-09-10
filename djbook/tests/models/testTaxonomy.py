from django.test import TestCase
from djbook.models import Taxonomy


# https://docs.djangoproject.com/en/3.1/topics/testing/advanced/#using-different-testing-frameworks

class TestTaxonomy(TestCase):
    """Тестирует класс Taxonomy."""

    def setUp(self):
        self.parent = Taxonomy.objects.create(
            eng_word='By themes',
            rus_word='По темам',
            parent=None,
            slug='themes'
        )
        self.tax = Taxonomy.objects.create(
            eng_word='food and meals',
            rus_word='продукты питания',
            parent=self.parent,
            slug='food-and-meals'
        )
        self.kid1 = Taxonomy.objects.create(
            eng_word='fruits',
            rus_word='фрукты',
            parent=self.tax,
            slug='fruits'
        )
        self.kid2 = Taxonomy.objects.create(
            eng_word='vegetables',
            rus_word='овощи',
            parent=self.tax,
            slug='vegetables'
        )

    def test_get_kids_rus(self):
        expected = self.tax.get_kids_rus()
        actual = self.kid2.rus_word + ', ' + self.kid1.rus_word
        self.assertEqual(expected, actual)

    def test_get_parent_rus(self):
        expected = self.parent.rus_word
        actual = self.tax.get_parent_rus()
        self.assertEqual(expected, actual)

    def test_save_with_no_slug(self):
        tax = Taxonomy.objects.create(
            eng_word='Most frequent english words',
            rus_word='Наиболее частые английские слова',
            parent=None
        )
        expected = 'most-frequent-english-words'
        actual = tax.slug
        self.assertEqual(expected, actual)

    def test_str(self):
        expected = f'Taxonomy{{id:{self.tax.id}, eng:food and meals, '
        expected += f'rus:продукты питания, parent_id:{self.parent.id}}}'
        actual = self.tax.__str__()
        self.assertEqual(expected, actual)
