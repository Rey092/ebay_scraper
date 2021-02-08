import csv

import pandas as pd  # excel
from PyQt5 import QtCore
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

profile = webdriver.FirefoxProfile()
# PROXY_HOST = "12.12.12.123"
# PROXY_PORT = "1234"
# profile.set_preference("network.proxy.type", 1)
# profile.set_preference("network.proxy.http", PROXY_HOST)
# profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()
desired = DesiredCapabilities.FIREFOX

options = webdriver.FirefoxOptions()
options.set_preference("dom.webnotifications.serviceworker.enabled", False)
options.set_preference("dom.webnotifications.enabled", False)
options.add_argument('--headless')


def scraper(key, progressbar, push, line):
    rozetka_items = []
    driver = webdriver.Firefox(options=options, desired_capabilities=desired, firefox_profile=profile)
    driver.get('https://ebay.com')
    xpath_form = "/html/body/header/table/tbody/tr/td[3]/form/table/tbody/tr/td[1]/div[1]/div/input[1]"
    driver.find_element_by_xpath(xpath_form).send_keys(key)
    xpath_find = "/html/body/header/table/tbody/tr/td[3]/form/table/tbody/tr/td[3]/input"
    driver.find_element_by_xpath(xpath_find).click()
    current_url = driver.current_url
    breaker = ""

    for page in range(1, 51):
        driver.get(f"{current_url}&_ipg=200&_pgn={page}")
        print("Page {} is uploaded".format(page))
        QtCore.QMetaObject.invokeMethod(progressbar, "setValue",
                                        QtCore.Qt.QueuedConnection,
                                        QtCore.Q_ARG(int, page * 2))
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # Lets cook the soup.
        # Extract data according to instructions to 'info' and store it into 'rozetka_items'
        products = soup.select('div.s-item__info')

        if str(breaker) == f"0 results for {key}":
            break

        try:
            breaker = soup.select('.srp-controls__count-heading')[0].text
            if str(breaker) == f"0 results for {key}":
                break
        except IndexError:
            pass

        for elem in products:
            try:
                title = elem.select('.s-item__title')[0].text
            except IndexError:
                title = "title error"
            try:
                stars = elem.select('span.clipped')[0].text \
                    .replace(" out of 5 stars.", "")
                stars = "0" if "." not in stars else stars
            except IndexError:
                stars = "0"

            try:
                price = elem.select('span.s-item__price')[0].text \
                    .replace(",", "") \
                    .replace("$", "")

            except IndexError:
                min_price = "no price"
                max_price = "no price"
            else:
                if "to" in price:
                    min_price = price.split()[0]
                    max_price = price.split()[-1]
                else:
                    min_price = price
                    max_price = price

            try:
                hotness = elem.select('span.s-item__hotness')[0].text.split()[0] \
                    .replace(",", "") \
                    .replace("+", "") \
                    .replace("Hot", "0") \
                    .replace("Almost", "0") \
                    .replace("Last", "0") \
                    .replace("Certified", "0") \
                    .replace("Benefits", "0")
            except IndexError:
                hotness = "0"

            info = {
                "Title": title.strip(),
                "Stars": stars,
                "Min Price": min_price,
                "Max Price": max_price,
                "Sold": hotness,
            }
            rozetka_items.append(info)
    driver.close()

    keys = rozetka_items[0].keys()  # get keys from 'rozetka_items'
    with open(f'data\\{key}.csv', 'w', newline='', encoding="UTF-8") as output_file:  # write .csv
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(rozetka_items)
    read_file = pd.read_csv(f'data\\{key}.csv')  # read csv with 'pandas' and convert it then
    read_file.to_excel(f'data\\{key}.xlsx', index=None, header=True)
    QtCore.QMetaObject.invokeMethod(progressbar, "setValue",
                                    QtCore.Qt.QueuedConnection,
                                    QtCore.Q_ARG(int, 100))
    QtCore.QMetaObject.invokeMethod(push, "setEnabled",
                                    QtCore.Qt.QueuedConnection,
                                    QtCore.Q_ARG(bool, True))
    QtCore.QMetaObject.invokeMethod(line, "setEnabled",
                                    QtCore.Qt.QueuedConnection,
                                    QtCore.Q_ARG(bool, True))
    print("\ndone")
