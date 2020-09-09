from selenium import webdriver

# Версия webdriver Chrome должна совпадать с версией браузера.
# https://sites.google.com/a/chromium.org/chromedriver/home
browser = webdriver.Chrome('/home/cyberbotx/downloads/chromedriver')
browser.get('http://django.bot.net/')

# Если проверка не прошла, возбуждается исключение AssertionError.
assert 'Главная страница' in browser.title

# Закрыть окно браузера.
browser.close()
# Выйти из браузера.
# browser.quit()
