import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def get_cards() -> list:
    service_data = []
    driver.get("https://bank.forte.kz/ru/cards")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    divs = soup.find_all("div", class_="MuiContainer-root sc-cDvQBt bmGOiM MuiContainer-maxWidthLg")
    for div in divs:
        try:
            name = div.find("h3").text.strip()
        except AttributeError:
            name = "null"
        try:
            url = div.find("a").get("href", None)
        except AttributeError:
            url = "null"
        selectors = ["p", "span"]
        description = []

        for desc_selector in selectors:
            description_element = div.find(desc_selector)
            if desc_selector == "span":
                if description_element is None:
                    continue
                raw_text = description_element.get_text(strip=True)
            else:
                if description_element is None:
                    continue
                raw_text = description_element.text.strip()
            description.append(raw_text)

        if not description:
            description = "null"
        else:
            description = " ".join(description)
        service_data.append({
            "service_name": "карта",
            "name": name,
            "description": description,
            "url": url if url else "null"
        })
    return service_data

def get_credits() -> list:
    service_data = []
    driver.get("https://bank.forte.kz/ru/credits")
    time.sleep(20)
    detail_buttons = driver.find_elements(By.XPATH, '//a[.="Подробнее"]')

    for btn in detail_buttons:
        try:
            card = btn.find_element(By.XPATH, './ancestor::div[3]')
            pre_card = btn.find_element(By.XPATH, './ancestor::div[2]')
            name_el = card.find_element(By.XPATH, './/span[1]')
            desc_el = pre_card.find_element(By.XPATH, './/span[1]')
            url = btn.get_attribute("href")
            service_data.append({
                "service_name": "кредит",
                "name": name_el.text.strip(),
                "description": desc_el.text.strip(),
                "url": url if url else "null"
            })

        except Exception as e:
            pass
    return service_data

def get_deposits() -> list:
    service_data = []
    driver.get("https://bank.forte.kz/ru/deposits")
    time.sleep(20)
    deposit_cards = driver.find_elements(By.XPATH, '//div[contains(@class, "MuiCard-root")]')
    for card in deposit_cards:
        try:
            name_el = card.find_element(By.XPATH, './/p[1]')
            name = name_el.text.strip()
            desc_el = card.find_element(By.XPATH, './/p[2]')
            description = desc_el.text.strip()
            link_el = card.find_element(By.XPATH, './/a[.="Подробнее"]')
            url = link_el.get_attribute("href")
            service_data.append({
                "service_name": "депозит",
                "name": name,
                "description": description,
                "url": url if url else "null"
            })

        except Exception as e:
            pass
    return service_data

def get_transfers() -> list:
    service_data = []
    driver.get("https://bank.forte.kz/ru/transfers")
    time.sleep(20)
    detail_buttons = driver.find_elements(By.XPATH, '//a[.="Подробнее"]')

    for btn in detail_buttons:
        try:
            card = btn.find_element(By.XPATH, './ancestor::div[3]')
            pre_card = btn.find_element(By.XPATH, './ancestor::div[2]')
            name_el = card.find_element(By.XPATH, './/span[1]')
            desc_el = pre_card.find_elements(By.XPATH, './/span')
            descs = ""
            for desc in desc_el:
                descs += desc.text.strip() + " "
            url = btn.get_attribute("href")
            service_data.append({
                "service_name": "перевод",
                "name": name_el.text.strip(),
                "description": descs,
                "url": url if url else "null"
            })

        except Exception as e:
            pass
    return service_data

def get_salary_projects() -> list:
    service_data = []
    driver.get("https://bank.forte.kz/ru/salary-project")
    time.sleep(20)
    sps = driver.find_elements(By.XPATH, '//div[contains(@class, "sc-knSEWW")]')
    for sp in sps:
        try:
            name = sp.find_element(By.XPATH, './/h2')
            name_text = name.text.strip() if name else "null"
            description = ""
            descs = sp.find_elements(By.XPATH, './/p')
            for desc in descs:
                description += desc.text.strip() + "\n"
            service_data.append({
                "service_name": "зарплатный проект",
                "name": name_text,
                "description": description,
                "url": "null"
            })

        except Exception as e:
            pass
    return service_data

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["service_name", "name", "description", "url"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    """
    Scrapes cards, credits, deposits, transfers, and salary projects from the Forte Bank website.
    Uses Selenium and BeautifulSoup for web scraping.
    Gets name, description, and URL for each service, if available.
    Saves the data to a CSV file named "services.csv" in the "data/raw" directory.
    Initializes the Chrome WebDriver using the webdriver_manager package to handle driver installation.
    Closes the WebDriver after scraping all data.
    :return: None
    """

    all_data = []
    all_data.extend(get_cards())
    all_data.extend(get_credits())
    all_data.extend(get_deposits())
    all_data.extend(get_transfers())
    all_data.extend(get_salary_projects())

    save_to_csv(all_data, "data/raw/services.csv")
    driver.quit()

