from selenium import webdriver
import unittest

# Запуск.
# python -m unittest functional_test.py

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


class VisitorTest(unittest.TestCase):
    """Тест нового посетителя"""

    def setUp(self):
        self.browser = webdriver.Chrome('/home/cyberbotx/downloads/chromedriver')

    def tearDown(self):
        self.browser.close()

    def test_home_page_title(self):
        """Проверить title страницы."""
        self.browser.get('http://django.bot.net/')
        self.assertEqual('Главная страница', self.browser.title)
