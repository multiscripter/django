from unittest import skip

from django.test import TestCase
from djbook.views import build_tree
from djbook.views import build_html_by_tree
from .models import Taxonomy


class ViewsTest(TestCase):
    def setUp(self):
        data = [
            ['By themes', 'По темам', None, 'themes'],
            ['Most frequent english words', 'Наиболее частые английские слова',
             None, 'most-frequent-english-words'],
            ['food and meals', 'пищевые продукты и питание', 1, 'food-and-meals'],
            ['fruits', 'фрукты', 3, 'fruits'],
            ['vegetables', 'овощи', 3, 'vegetables'],
            ['transportation', 'транспорт', 1, 'transport'],
            ['things', 'вещи', 1, 'things'],
            ['1st 1000 words', '1-ая 1000 слов', 2, '1st-1000-words'],
            ['2nd 1000 words', '2-ая 1000 слов', 2, '2nd-1000-words']
        ]
        # Пакетное добавление (одна транзакция).
        Taxonomy.objects.bulk_create(
            Taxonomy(
                eng_word=a[0], rus_word=a[1], parent_id=a[2], slug=a[3]
            ) for a in data
        )

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
