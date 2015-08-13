from selenium.webdriver import Firefox
from contextlib import closing
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display

URL = 'http://fanserials.tv/index.php?do=search'

series = [
#   ('name',                   'season', 'series')
    ('гримм',                  '4',      '21')
]

def find_series_fanserials(browser, data):
    name = data[0] + ' ' + data[1] + ' сезон ' + data[2] + ' серия'
    rv = ''

    elem = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.NAME, 'story'))
    )

#    elem.click()
    elem.clear()
    elem.send_keys(name)
    elem.send_keys(Keys.RETURN)

    try:

        articles = browser.find_elements_by_css_selector('article')
        for article in articles:
            h5 = article.find_element_by_tag_name('h5')
            if (name.lower() in h5.text.lower()):
                a = h5.find_element_by_partial_link_text(data[1] + ' сезон')
                rv = a.text + ' | ' + a.get_attribute('href')

    except NoSuchElementException:
        pass

    if rv:
        print('\n', rv)
    else:
        print('.', end='')

def main():
    display = Display(visible=0, size=(800, 600))
    display.start()

    with closing(Firefox()) as browser:
        print('\n[' + URL +']')
        browser.get(URL)

        for data in series:
            find_series_fanserials(browser, data)

    display.stop()


if __name__ == "__main__":
    main()
