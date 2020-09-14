from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# Тестирование с использованием LiveServer.
# LiveServer создаёт тестовую БД.
# python manage.py test djbook.tests.functional.testFormsPage


class PageFormsTest(LiveServerTestCase):
    """Тест страницы форм с использование LiveServer"""

    def setUp(self):
        self.browser = webdriver.Chrome('/home/cyberbotx/downloads/chromedriver')
        self.browser.get(self.live_server_url + '/forms/')
        self.url = self.browser.current_url

    def test_can_start_list_and_get_it_later(self):
        """Тест: начать список итемов и получить его позже."""

        # Получить атрибут html-элемента.
        # text_field.get_attribute('attr_name')
        # Получить свойство html-элемента.
        # text_field.get_property('prop_name')

        for num in range(1, 3):
            text_field = self.browser.find_element_by_id('form-2-text')
            # Ввести текст в поле ввода.
            text_field.send_keys(f'Папа Бенедикт {num}')
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
            go_back = self.browser.find_element_by_id('go-back')
            go_back.click()

        time.sleep(2)
        # https://selenium-python.readthedocs.io/locating-elements.html
        rows = self.browser.find_elements_by_css_selector('#items-table tbody tr')
        self.assertTrue(
            any('Папа Бенедикт 2' in row.text for row in rows)
        )

    def tearDown(self):
        self.browser.close()
