from django.test import TestCase
from djbook.views import build_tree
from djbook.views import build_html_by_tree
from djbook.views import get_kids
from unittest import skip
from .models import Taxonomy


class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Действия перед всеми тестами.
        При переопределении setUpClass(cls) всегда нужно вызывать
        метод super(%имя_текущего_класса_тестов%, cls).setUpClass()"""
        super(ViewsTest, cls).setUpClass()

    def setUp(self):
        data = [
            ['By themes', 'По темам', None, 'themes'],
            ['Most words', 'частые слова', None, 'most-words'],
            ['food and meals', 'продукты питания', 1, 'food-and-meals'],
            ['fruits', 'фрукты', 3, 'fruits'],
            ['vegetables', 'овощи', 3, 'vegetables'],
            ['transportation', 'транспорт', 1, 'transport'],
            ['things', 'вещи', 1, 'things'],
            ['1st 1000 words', '1-ая 1000 слов', 2, '1st-1000-words'],
            ['2nd 1000 words', '2-ая 1000 слов', 2, '2nd-1000-words']
        ]
        a = 0
        for tax in data:
            parent = data[tax[2] - 1] if tax[2] is not None else None
            data[a] = Taxonomy.objects.create(
                eng_word=tax[0], rus_word=tax[1], parent=parent, slug=tax[3]
            )
            a += 1

        self.tax_set = Taxonomy.objects.all().order_by('eng_word')

    @skip("Don't want to test")
    def test_build_tree(self):
        """Tests Node build_tree(tax_id)"""
        tree = build_tree(self.tax_set, 1)
        self.assertTrue(len(tree.kids))

    def test_build_html_by_tree(self):
        """Tests String build_html_by_tree(tree)"""
        tree = build_tree(self.tax_set, 1)
        tree_html = build_html_by_tree(tree)
        self.assertTrue(tree_html)

    # python manage.py test djbook.tests.ViewsTest.test_get_kids_throws_exception
    # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaises
    def test_get_kids_throws_exception(self):
        """Тестирует Node[] get_kids(tax_set, node)"""
        self.assertRaises(AttributeError, get_kids, [1, 2], None)

    @classmethod
    def tearDownClass(cls):
        """Действия после всех тестов.
        При переопределении tearDownClass(cls) всегда нужно вызывать
        метод super(%имя_текущего_класса_тестов%, cls).tearDownClass()"""
        super(ViewsTest, cls).tearDownClass()
