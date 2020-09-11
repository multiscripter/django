from selenium import webdriver
import unittest

# Запуск.
# Из папки с тестом.
# python -m unittest pageHomeTest.py
# Из корневой папки сайта.
# python -m unittest djbook/tests/functional/pageHomeTest.py
# Из корневой папки сайта. Все файлы тестов.
# python -m unittest djbook/tests/functional/*.py

# Версия webdriver Chrome должна совпадать с версией браузера.
# https://sites.google.com/a/chromium.org/chromedriver/home
# browser = webdriver.Chrome('/home/cyberbotx/downloads/chromedriver')
# browser.get('http://django.bot.net/')

# Если проверка не прошла, возбуждается исключение AssertionError.
# assert 'Главная страница' in browser.title

# Закрыть окно браузера.
# browser.close()
# Выйти из браузера.
# browser.quit()


class PageHomeTest(unittest.TestCase):
    """Тест домашней страницы."""

    def setUp(self):
        self.browser = webdriver.Chrome('/home/cyberbotx/downloads/chromedriver')

    def tearDown(self):
        self.browser.close()

    def test_home_page(self):
        """Тестирует главную страницу."""
        self.browser.get('http://django.bot.net/')

        # Сравнить заголовок страницы.
        self.assertEqual('Главная страница', self.browser.title)
        # Сравнить h1 страницы.
        actual = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('Сайт на Джанге', actual)
