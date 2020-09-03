from unittest import skip

from django.test import TestCase

from .models import Taxonomy
from djbook.views import build_tree
from djbook.views import build_html_by_tree


def create_tax(eng, rus, p_id=None):
    Taxonomy.objects.create(eng_word=eng, rus_word=rus, parent_id=p_id)


class ViewsTest(TestCase):
    def setUp(self):
        create_tax('By themes', 'По темам')
        create_tax('Most frequent english words', 'Наиболее частые английские слова')
        create_tax('food and meals', 'пищевые продукты и питание', 1)
        create_tax('fruits', 'фрукты', 3)
        create_tax('vegetables', 'овощи', 3)
        create_tax('transportation', 'транспорт', 1)
        create_tax('things', 'вещи', 1)
        create_tax('1st 1000 words', '1-ая 1000 слов', 2)
        create_tax('2nd 1000 words', '2-ая 1000 слов', 2)

    @skip("Don't want to test")
    def test_build_tree(self):
        """Tests None build_tree(tax_id)"""
        tree = build_tree(1)
        self.assertTrue(len(tree.kids))

    def test_build_html_by_tree(self):
        """Tests String build_html_by_tree(tree)"""
        tree = build_tree(1)
        tree_html = build_html_by_tree(tree)
        # print(tree_html)
        self.assertTrue(tree_html)
