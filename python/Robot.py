from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import GoogleTranslate
import KeywordDict

BROWSER_OPTION = webdriver.ChromeOptions()
BROWSER_OPTION.add_argument("headless")
HEADERS = ({'User-Agent':'Chrome/44.0.2403.157'})

GOOGLE_SEARCH_BAR = '//input[@name="q"]'
GOOGLE_RESULT_HREF = '//div[@id="search"]//div[@class="yuRUbf"]/a'

## 處理搜尋結果出現重複的情況
def removeIdentical(result):
    occurrence_list = []
    out_list = []
    for res in result:
        if res[1] == '':
            out_list.append(res)
        else:
            if res[1] in occurrence_list:
                out_list.append(['',''])
            else:
                occurrence_list.append(res[1])
                out_list.append(res)
    return out_list

## 使用google search
def google_search(keyword, site, number):

    print(f"Using google search, site: {site}")

    out_list = []

    regex = "http[s]?://[^/]+"
    temp = re.findall(regex,site)[0]

    browser = webdriver.Chrome(options=BROWSER_OPTION)
    try:
        browser.get("https://www.google.com/")
        search_bar = browser.find_element(by=By.XPATH,value=GOOGLE_SEARCH_BAR)
        search_bar.send_keys(keyword + " site:" + temp + Keys.ENTER)
        WebDriverWait(browser,10).until(expected_conditions.presence_of_element_located((By.XPATH, GOOGLE_RESULT_HREF)))
        hrefs = browser.find_elements(by=By.XPATH,value=GOOGLE_RESULT_HREF)
        titles = browser.find_elements(by=By.XPATH,value=GOOGLE_RESULT_HREF + '/h3')
        for i in range(number):
            href = hrefs[i].get_attribute('href')
            title = titles[i].text
            out_list.append([href,title])
    except:
        for i in range(len(out_list), number):
            out_list.append(['',''])

    browser.quit()

    out_list = removeIdentical(out_list)
    
    return out_list

## 回傳絕對路徑
def process_href(homepage, href):
    if href.startswith("http"):
        return href
    else:
        regex = "http[s]?://[^/]+"
        temp = re.findall(regex,homepage)
        url = ""
        if len(temp) > 0:
            url = temp[0] + href
        else:
            if homepage.endswith('/'):
                url = homepage[:-1]+href
            else:
                url = homepage + href
        return url

## 取得bs4元素內所有文字
def get_itertext(itertext):
    out = ''
    for text in itertext:
        if len(re.findall('[^\n\t ]+',text)) > 0:
            out+=text+' '
    out = out.replace('\n',' ')
    out = out.replace('\t',' ')
    return out

def get_href_title(homepage, url, xpaths, keyword=''):

    out_list = []
    
    try:
        soup = BeautifulSoup(requests.get(url, headers=HEADERS).content, "lxml")
        dom = etree.HTML(str(soup))
        for i in range (len(xpaths)):
            href = dom.xpath(xpaths[i][0])[0].get("href")
            href = process_href(homepage, href)
            title = get_itertext(dom.xpath(xpaths[i][1])[0].itertext())
            out_list.append([href,title])
    except:
        browser = webdriver.Chrome(options=BROWSER_OPTION)
        try:
            browser.maximize_window()
            browser.get(url)
            WebDriverWait(browser,7).until(expected_conditions.presence_of_element_located((By.XPATH, xpaths[0][0])))
            html = browser.page_source
            soup = BeautifulSoup(html, "lxml")
            dom = etree.HTML(str(soup))
            for i in range (len(out_list), len(xpaths)):
                href = dom.xpath(xpaths[i][0])[0].get("href")
                title = get_itertext(dom.xpath(xpaths[i][1])[0].itertext())
                href = process_href(homepage, href)
                out_list.append([href,title])
        except:
            failure_count = len(xpaths) - len(out_list)
            if url==homepage:
                for i in range(failure_count):
                    out_list.append(['',''])
            else:
                to_search = keyword if type(keyword)==str else keyword[0]
                results = google_search(to_search, homepage, failure_count)
                for result in results:
                    out_list.append(result)
        browser.quit()

    out_list = removeIdentical(out_list)

    return out_list
    

class Robot1:
    def __init__(self, arg):
        self.args = arg
    
    def get_homepage(self):
        output = {}
        contents = []
        contents = get_href_title(self.args["homepage1"],self.args["homepage1"],self.args["xpath_homepage"])
        output.update({self.args["code"]:contents})
        return output

    def search_keyword(self, keyword):
        output = {}
        contents = []
        code = self.args["code"]
        print(f"{code} receiving {keyword} to search")

        to_search = KeywordDict.search_keyword_dict(keyword, self.args["language1"])
        if to_search==keyword:
            translated = GoogleTranslate.translate_text([keyword],self.args["language1"])
            to_search = translated[0]['translatedText']
        
        print(f"{code} searching translated keyword: {to_search}")

        keyword_string = to_search.replace(" ",self.args["search1"][1])
        search_url = self.args["search1"][0]+keyword_string+self.args["search1"][2]
        contents = get_href_title(self.args["homepage1"],search_url,self.args["xpath_search"],to_search)
        output.update({self.args["code"]:contents})
        return output

class Robot2:
    def __init__(self, arg):
        self.args = arg
    
    def get_homepage(self):
        output = {}
        contents = []
        content1 = get_href_title(self.args["homepage1"],self.args["homepage1"],self.args["xpath_homepage"][0:3])
        content2 = get_href_title(self.args["homepage2"],self.args["homepage2"],self.args["xpath_homepage"][3:])
        contents = content1 + content2
        output.update({self.args["code"]:contents})
        return output

    def search_keyword(self, keyword):
        output = {}
        contents = []
        code = self.args["code"]
        print(f"{code} receiving {keyword} to search")

        to_search = KeywordDict.search_keyword_dict(keyword, self.args["language1"])
        if to_search==keyword:
            translated = GoogleTranslate.translate_text([keyword],self.args["language1"])
            to_search = translated[0]['translatedText']
        print(f"{code} searching translated keyword: {to_search}")
        

        keyword_string = to_search.replace(" ",self.args["search1"][1])
        search_url = self.args["search1"][0]+keyword_string+self.args["search1"][2]
        content1 = get_href_title(self.args["homepage1"],search_url,self.args["xpath_search"][0:3],to_search)

        keyword_string = to_search.replace(" ",self.args["search2"][1])
        search_url = self.args["search2"][0]+keyword_string+self.args["search2"][2]
        content2 = get_href_title(self.args["homepage2"],search_url,self.args["xpath_search"][3:],to_search)

        contents = content1 + content2
        output.update({self.args["code"]:contents})
        return output

class Robot0:
    def __init__(self, arg):
        self.args = arg
    
    def get_homepage(self):
        output = {}
        contents = []
        content1 = get_href_title(self.args["homepage1"],self.args["homepage1"],self.args["xpath_homepage"][0:3])
        content2 = get_href_title(self.args["homepage2"],self.args["homepage2"],self.args["xpath_homepage"][3:])
        contents = content1 + content2
        output.update({self.args["code"]:contents})
        return output

    def search_keyword(self, keyword):
        output = {}
        contents = []
        code = self.args["code"]
        print(f"{code} receiving {keyword} to search")

        to_search = KeywordDict.search_keyword_dict(keyword, self.args["language1"])
        if to_search==keyword:
            translated = GoogleTranslate.translate_text([keyword],self.args["language1"])
            to_search = translated[0]['translatedText']
        print(f"{code} searching translated keyword: {to_search}")

        keyword_string = to_search.replace(" ",self.args["search1"][1])
        search_url = self.args["search1"][0]+keyword_string+self.args["search1"][2]
        content1 = get_href_title(self.args["homepage1"],search_url,self.args["xpath_search"][0:3],to_search)

        to_search = KeywordDict.search_keyword_dict(keyword, self.args["language2"])
        if to_search==keyword:
            translated = GoogleTranslate.translate_text([keyword],self.args["language2"])
            to_search = translated[0]['translatedText']

        keyword_string = to_search.replace(" ",self.args["search2"][1])
        search_url = self.args["search2"][0]+keyword_string+self.args["search2"][2]
        content2 = get_href_title(self.args["homepage2"],search_url,self.args["xpath_search"][3:],to_search)

        contents = content1 + content2
        output.update({self.args["code"]:contents})
        return output

class Robot3:
    def __init__(self, arg):
        self.args = arg
    
    def get_homepage(self):
        output = {}
        contents = []
        content1 = get_href_title(self.args["homepage1"],self.args["homepage1"],self.args["xpath_homepage"][0:2])
        content2 = get_href_title(self.args["homepage2"],self.args["homepage2"],self.args["xpath_homepage"][2:4])
        content3 = get_href_title(self.args["homepage3"],self.args["homepage3"],self.args["xpath_homepage"][4:])
        contents = content1 + content2 + content3
        output.update({self.args["code"]:contents})
        return output

    def search_keyword(self, keyword):
        output = {}
        contents = []
        code = self.args["code"]
        print(f"{code} receiving {keyword} to search")

        to_search = KeywordDict.search_keyword_dict(keyword, self.args["language1"])
        if to_search==keyword:
            translated = GoogleTranslate.translate_text([keyword],self.args["language1"])
            to_search = translated[0]['translatedText']
        print(f"{code} searching translated keyword: {to_search}")

        keyword_string = to_search.replace(" ",self.args["search1"][1])
        search_url = self.args["search1"][0]+keyword_string+self.args["search1"][2]
        content1 = get_href_title(self.args["homepage1"],search_url,self.args["xpath_search"][0:2],to_search)

        keyword_string = to_search.replace(" ",self.args["search2"][1])
        search_url = self.args["search2"][0]+keyword_string+self.args["search2"][2]
        content2 = get_href_title(self.args["homepage2"],search_url,self.args["xpath_search"][2:4],to_search)

        keyword_string = to_search.replace(" ",self.args["search3"][1])
        search_url = self.args["search3"][0]+keyword_string+self.args["search3"][2]
        content3 = get_href_title(self.args["homepage3"],search_url,self.args["xpath_search"][4:],to_search)

        contents = content1 + content2 + content3
        output.update({self.args["code"]:contents})
        return output

class HomepageGreenLand:

    def __init__(self):
        self.code = "GL"
        self.language1 = "da"
        self.homepage1 = "https://sermitsiaq.ag"
        self.xpath_homepage = [['//*[@id="frontpage"]/section[3]/div[1]/div[1]/a','//*[@id="frontpage"]/section[3]/div[1]/div[1]/a/article/h1'],
                               ['//*[@id="frontpage"]/section[3]/div[1]/div[2]/a[1]','//*[@id="frontpage"]/section[3]/div[1]/div[2]/a[1]/article/h1'],
                               ['//*[@id="frontpage"]/section[3]/div[1]/div[2]/a[2]','//*[@id="frontpage"]/section[3]/div[1]/div[2]/a[2]/article/h1'],
                               ['//*[@id="frontpage"]/section[5]/div[1]/div/a','//*[@id="frontpage"]/section[5]/div[1]/div/a/article/h1'],
                               ['//*[@id="frontpage"]/section[7]/div[1]/a[1]','//*[@id="frontpage"]/section[7]/div[1]/a[1]/article/h1']]

    def get_homepage(self):
        output = {}
        contents = []
        contents = get_href_title(self.homepage1,self.homepage1,self.xpath_homepage)
        output.update({self.code:contents})
        return output

    def search_keyword(self, keyword):
        output = {}
        contents = []

        print(f"{self.code} receiving {keyword} to search")
        translated = GoogleTranslate.translate_text([keyword],self.language1)
        translated_keyword = translated[0]['translatedText']
        print(f"{self.code} searching translated keyword: {translated_keyword}")

        contents = google_search(translated_keyword, self.homepage1, 5)
        
        output.update({self.code:contents})
        return output


class RobotChina:
    def __init__(self):
        self.code = "CN"
        self.language1 = "zh-CN"
        self.homepage1 = "http://www.xinhuanet.com"
        self.homepage2 = "http://www.people.com.cn"
        self.xpath_homepage = [['//*[@id="depthFocus"]/div[2]/div[1]/div[1]/a','//*[@id="depthFocus"]/div[2]/div[1]/div[1]/a'],
                               ['//*[@id="depthFocus"]/div[2]/div[2]/div[1]/a','//*[@id="depthFocus"]/div[2]/div[2]/div[1]/a'],
                               ['//*[@id="depthFocus"]/div[2]/div[3]/div[1]/a','//*[@id="depthFocus"]/div[2]/div[3]/div[1]/a'],
                               ['//*[@id="rm_bq"]/div[2]/ul[1]/li[1]/a','//*[@id="rm_bq"]/div[2]/ul[1]/li[1]/a'],
                               ['//*[@id="rm_bq"]/div[2]/ul[1]/li[2]/a','//*[@id="rm_bq"]/div[2]/ul[1]/li[2]/a']]

    def get_homepage(self):
        output = {}
        contents = []
        contents = get_href_title(self.homepage1,self.homepage1,self.xpath_homepage)
        output.update({self.code:contents})
        return output

    def search_keyword(self, keyword):
        output = {}
        contents = []

        print(f"{self.code} receiving {keyword} to search")
        translated = GoogleTranslate.translate_text([keyword],self.language1)
        translated_keyword = translated[0]['translatedText']
        print(f"{self.code} searching translated keyword: {translated_keyword}")

        content1 = google_search(translated_keyword, self.homepage1, 3)
        content2 = google_search(translated_keyword, self.homepage2, 2)
        contents = content1 + content2

        output.update({self.code:contents})
        return output