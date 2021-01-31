import csv  # for .csv creation
import itertools  # for infinite "for loop"

import pandas as pd  # excel
from bs4 import BeautifulSoup  # get information from raw data
from selenium import webdriver


def scraper(key_word):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    # options.add_argument('--headless')
    options.add_argument("start-maximized")
    # Exclude the collection of enable-automation switches
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # Turn-off useAutomationExtension
    options.add_experimental_option('useAutomationExtension', False)

    # Set driver
    driver = webdriver.Chrome('chromedriver', options=options)
    # Change the property value of the navigator for driver to undefined
    driver.execute_script("Object.defineProperty(navigator, 'driver', {get: () => undefined})")
    # Rotating the user-agent through execute_cdp_cmd() command as follows:
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/83.0.4103.53 Safari/537.36'})

    rozetka_items = []
    keyword = key_word

    driver.get('https://ebay.com')
    xpath_form = "/html/body/header/table/tbody/tr/td[3]/form/table/tbody/tr/td[1]/div[1]/div/input[1]"
    driver.find_element_by_xpath(xpath_form).send_keys(keyword)
    xpath_find = "/html/body/header/table/tbody/tr/td[3]/form/table/tbody/tr/td[3]/input"
    driver.find_element_by_xpath(xpath_find).click()
    currentURL = driver.current_url
    print(currentURL)
    "&_ipg=200&_pgn=2"

    for page in itertools.count(start=1):
        if page == 51:
            break
        driver.get(f"{currentURL}&_ipg=200&_pgn={page}")

        print("Page {} is uploaded".format(page))

        soup = BeautifulSoup(driver.page_source, 'html5lib')  # Lets cook the soup.
        # Extract data according to instructions to 'info' and store it into 'rozetka_items'
        products = soup.select('div.s-item__info')
        breaker = soup.select('.srp-controls__count-heading')[0].text
        if breaker == f"0 results for {keyword}" or not products:
            break
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
        page += 1

    keys = rozetka_items[0].keys()  # get keys from 'rozetka_items'
    with open('products.csv', 'w', newline='', encoding="UTF-8") as output_file:  # write .csv
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(rozetka_items)

    read_file = pd.read_csv(r'products.csv')  # read csv with 'pandas' and convert it then
    read_file.to_excel(r'products.xlsx', index=None, header=True)
    driver.close()
