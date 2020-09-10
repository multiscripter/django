# Закомментированные строки позволяют запускать тесты из PyCharm, но
# используются настройки из djbook.settings.py. Т.е. боевая БД и прочее.
# Нужно морочить rollback, другую БД или in-memory СУБД для тестов.
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djbook.settings")
# django.setup()
from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from djbook.views import build_tree, home
from djbook.views import build_html_by_tree
from djbook.views import get_kids
from unittest import skip
from djbook.models import Taxonomy


# https://docs.djangoproject.com/en/3.1/topics/testing/advanced/#using-different-testing-frameworks

# Покрытие кода.
# https://devguide.python.org/coverage/

# Стереть предыдущую информацию о покрытии.
# coverage erase
# Запустить все тесты с покрытием (из корня сайта).
# coverage run --source='.' --omit='*/migrations/*','*/polls/*' manage.py test
# Либо можно создать в корне сайта файл .coveragerc и в нём перечислить
# опции source, include и/или omit и их значения.
# https://coverage.readthedocs.io/en/coverage-5.2.1/source.html#source
# Собрать информацию в html-файлы.
# coverage html

# Запуск из консоли из корня сайта: python manage.py test djbook.tests.TestViews
class TestViews(TestCase):
    @classmethod
    def setUpClass(cls):
        """Действия перед всеми тестами.
        При переопределении setUpClass(cls) всегда нужно вызывать
        метод super(%имя_текущего_класса_тестов%, cls).setUpClass()"""
        super(TestViews, cls).setUpClass()

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

    @skip("Don't want to test")
    def test_build_html_by_tree(self):
        """Tests String build_html_by_tree(tree)"""
        tree = build_tree(self.tax_set, 1)
        tree_html = build_html_by_tree(tree)
        self.assertTrue(tree_html)

    # python manage.py test djbook.tests.TestViews.test_get_kids_throws_exception
    # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaises
    def test_get_kids_throws_exception(self):
        """Тестирует Node[] get_kids(tax_set, node)"""
        self.assertRaises(AttributeError, get_kids, [1, 2], None)

    def test_root_url_resolves_to_home_controller(self):
        """Тестирует отображение URI / на функцию home()"""

        # Найти функцию, на которую отображается указанный URI в urls.py.
        found = resolve('/')
        # Убедиться, что найденная функция - это функция home().
        self.assertEqual(found.func, home)

    def test_home_returns_html(self):
        """Тестирует, что ответом home() является html-страница."""
        request = HttpRequest()
        response = home(request)
        # Декодировать двоичный код в utf8-строку.
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertInHTML('<title>Главная страница</title>', html)
        self.assertTrue(html.endswith('</html>'))

    @classmethod
    def tearDownClass(cls):
        """Действия после всех тестов.
        При переопределении tearDownClass(cls) всегда нужно вызывать
        метод super(%имя_текущего_класса_тестов%, cls).tearDownClass()"""
        super(TestViews, cls).tearDownClass()
