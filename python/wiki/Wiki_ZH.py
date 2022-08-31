from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd
import time

BROWSER_OPTION = webdriver.ChromeOptions()
BROWSER_OPTION.add_argument("headless")

WIKI_URL_ZH = "https://zh.wikipedia.org/wiki/"
MATCH_REGEX = "https://[a-z]+\.wikipedia\.org/wiki/"
ENTITY_XPATH = '//*[@id="firstHeading"]'
OTHER_LANGUAGE_XPATH = '//*[@id="p-lang-label"]'
MORE_LANGUAGE_BUTTON_XPATH = '//*[@id="p-lang"]/div/ul/button'
SEARCH_LANGUAGE_XPATH = '//*[@id="search"]/div/div/input[2]'

LANGUAGE_CODE_DF = pd.read_excel("語言代碼對照表（維基用）.xlsx")

keyword = input("請輸入關鍵字")
browser = webdriver.Chrome()
browser.get(WIKI_URL_ZH+keyword)

try:
    WebDriverWait(browser,10).until(expected_conditions.presence_of_element_located((By.XPATH, OTHER_LANGUAGE_XPATH)))
    result_match = re.search(MATCH_REGEX, browser.current_url)
    if not type(result_match)==re.Match:
        print("No wiki page!!!")
    else:
        keyword_dict = pd.read_excel("語言代碼對照表（維基用）.xlsx")
        keyword_dict.insert(0, "原文", [keyword], False)
        
        for language in LANGUAGE_CODE_DF.columns:
            language_code = LANGUAGE_CODE_DF.loc[0, language]
            try:
                reference = browser.find_element(By.XPATH, '//a[@lang="'+language_code+'"]')
                browser.get(reference.get_attribute("href"))
                WebDriverWait(browser,10).until(expected_conditions.presence_of_element_located((By.XPATH, ENTITY_XPATH)))
                entity = browser.find_element(By.XPATH, ENTITY_XPATH).text
                entity = entity.replace("[編輯]","")
                keyword_dict.loc[0, language] = entity
                time.sleep(10)
            except:
                print("Not in first phase!!!")
                try:
                    more_language_button = browser.find_element(By.XPATH, MORE_LANGUAGE_BUTTON_XPATH)
                    more_language_button.click()
                    WebDriverWait(browser,10).until(expected_conditions.presence_of_element_located((By.XPATH, SEARCH_LANGUAGE_XPATH)))
                    search_language_input = browser.find_element(By.XPATH, SEARCH_LANGUAGE_XPATH)
                    search_language_input.send_keys(language)
                    WebDriverWait(browser,10).until(expected_conditions.presence_of_element_located((By.XPATH, '//a[@lang="'+language_code+'"]')))
                    reference = browser.find_element(By.XPATH, '//a[@lang="'+language_code+'"]')
                    browser.get(reference.get_attribute("href"))
                    WebDriverWait(browser,10).until(expected_conditions.presence_of_element_located((By.XPATH, ENTITY_XPATH)))
                    entity = browser.find_element(By.XPATH, ENTITY_XPATH).text
                    entity = entity.replace("[編輯]","")
                    keyword_dict.loc[0, language] = entity
                    time.sleep(10)
                except:
                    print("No this language!!!")
                    keyword_dict.loc[0, language] = "-"

        keyword_dict.to_excel(keyword+"字典.xlsx", index=False)
        
except Exception as e:
    print(e)

browser.quit()
