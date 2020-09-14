from djbook.models import Item
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

# https://www.selenium.dev/documentation/en/webdriver/browser_manipulation/

# Запуск.
# Из корневой папки сайта. Все файлы тестов.
# python manage.py test djbook.tests.functional
# или
# python -m unittest djbook/tests/functional/*.py
# Из корневой папки сайта. Класс тестов PageFormsTest.
# python manage.py test djbook.tests.functional.pageFormsTest


class PageFormsTest(unittest.TestCase):
    """Тест страницы форм."""

    def setUp(self):
        self.browser = webdriver.Chrome('/home/cyberbotx/downloads/chromedriver')
        self.browser.get('http://django.bot.net/forms/')
        self.url = self.browser.current_url

    def test_enter_text_in_name_field_and_send(self):
        text_field = self.browser.find_element_by_id('form-2-text')

        # Получить атрибут html-элемента.
        # text_field.get_attribute('attr_name')
        # Получить свойство html-элемента.
        # text_field.get_property('prop_name')

        # Ввести текст в поле ввода.
        text_field.send_keys('mister John Doe')
        # Нажать Enter.
        text_field.send_keys(Keys.ENTER)

        # Ожидать 5 секунд ответа сервера и редиректа на другую страницу.
        for a in range(0, 5):
            # Заснуть на секунду.
            time.sleep(1)
            if self.url != self.browser.current_url:
                break
        else:
            raise Exception('Страница не загрузилась за 5 секунд')

        # http://django.bot.net/forms-response/?status=ok&message=mister%20John%20Doe
        # Проверить, что целевой URI содержится в URL.
        self.assertTrue('/forms-response/' in self.browser.current_url)
        # Стравнить текст в h1.
        actual = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('Статус: ok', actual)

    def tearDown(self):
        Item.objects.filter(text='mister John Doe').delete()
        self.browser.close()
