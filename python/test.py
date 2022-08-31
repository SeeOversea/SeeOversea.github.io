# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import requests
# from bs4 import BeautifulSoup
# from lxml import etree
# import re
# import GoogleTranslate
# import KeywordDict

# BROWSER_OPTION = webdriver.ChromeOptions()
# BROWSER_OPTION.add_argument("headless")
# HEADERS = ({'User-Agent':'Chrome/44.0.2403.157'})

# GOOGLE_SEARCH_BAR = '//input[@name="q"]'
# GOOGLE_RESULT_HREF = '//div[@id="search"]//div[@class="yuRUbf"]/a'

# ## 使用google search
# def google_search(keyword, site, number):
#     out_list = []

#     regex = "http[s]?://[^/]+"
#     temp = re.findall(regex,site)[0]

#     browser = webdriver.Chrome(options=BROWSER_OPTION)
#     try:
#         browser.get("https://www.google.com/")
#         search_bar = browser.find_element(by=By.XPATH,value=GOOGLE_SEARCH_BAR)
#         search_bar.send_keys(keyword + " site:" + temp + Keys.ENTER)
#         WebDriverWait(browser,10).until(expected_conditions.presence_of_element_located((By.XPATH, GOOGLE_RESULT_HREF)))
#         hrefs = browser.find_elements(by=By.XPATH,value=GOOGLE_RESULT_HREF)
#         titles = browser.find_elements(by=By.XPATH,value=GOOGLE_RESULT_HREF + '/h3')
#         for i in range(number):
#             href = hrefs[i].get_attribute('href')
#             title = titles[i].text
#             out_list.append([href,title])
#     except:
#         for i in range(len(out_list), number):
#             out_list.append(['',''])

#     browser.quit()
#     return out_list

# ## 回傳絕對路徑
# def process_href(homepage, href):
#     if href.startswith("http"):
#         return href
#     else:
#         regex = "http[s]?://[^/]+"
#         temp = re.findall(regex,homepage)
#         url = ""
#         if len(temp) > 0:
#             url = temp[0] + href
#         else:
#             if homepage.endswith('/'):
#                 url = homepage[:-1]+href
#             else:
#                 url = homepage + href
#         return url

# ## 取得bs4元素內所有文字
# def get_itertext(itertext):
#     out = ''
#     for text in itertext:
#         if len(re.findall('[^\n\t ]+',text)) > 0:
#             out+=text+' '
#     out = out.replace('\n',' ')
#     out = out.replace('\t',' ')
#     return out

# def get_href_title(homepage, url, xpaths, keyword=''):

#     out_list = []
    
#     try:
#         soup = BeautifulSoup(requests.get(url, headers=HEADERS).content, "lxml")
#         dom = etree.HTML(str(soup))
#         for i in range (len(xpaths)):
#             href = dom.xpath(xpaths[i][0])[0].get("href")
#             href = process_href(homepage, href)
#             title = get_itertext(dom.xpath(xpaths[i][1])[0].itertext())
#             out_list.append([href,title])
#     except Exception:
#         browser = webdriver.Chrome(options=BROWSER_OPTION)
#         try:
#             browser.maximize_window()
#             browser.get(url)
#             WebDriverWait(browser,7).until(expected_conditions.presence_of_element_located((By.XPATH, xpaths[0][0])))
#             html = browser.page_source
#             soup = BeautifulSoup(html, "lxml")
#             dom = etree.HTML(str(soup))
#             for i in range (len(out_list), len(xpaths)):
#                 href = dom.xpath(xpaths[i][0])[0].get("href")
#                 title = get_itertext(dom.xpath(xpaths[i][1])[0].itertext())
#                 href = process_href(homepage, href)
#                 out_list.append([href,title])
#         except:
#             failure_count = len(xpaths) - len(out_list)
#             if url==homepage:
#                 for i in range(failure_count):
#                     out_list.append(['',''])
#             else:
#                 to_search = keyword if type(keyword)==str else keyword[0]
#                 results = google_search(to_search, homepage, failure_count)
#                 for result in results:
#                     out_list.append(result)
#         browser.quit()

#     return out_list
    

# class Robot1:
#     def __init__(self, arg):
#         self.args = arg
    
#     def get_homepage(self):
#         output = {}
#         contents = []
#         contents = get_href_title(self.args["homepage1"],self.args["homepage1"],self.args["xpath_homepage"])
#         output.update({self.args["code"]:contents})
#         return output

#     def search_keyword(self, keyword):
#         output = {}
#         contents = []
#         code = self.args["code"]
#         print(f"{code} receiving {keyword} to search")

#         to_search = KeywordDict.search_keyword_dict(keyword, self.args["language1"])
#         if to_search==keyword:
#             translated = GoogleTranslate.translate_text([keyword],self.args["language1"])
#             to_search = translated[0]['translatedText']
        
#         print(f"{code} searching translated keyword: {to_search}")

#         keyword_string = to_search.replace(" ",self.args["search1"][1])
#         search_url = self.args["search1"][0]+keyword_string+self.args["search1"][2]
#         contents = get_href_title(self.args["homepage1"],search_url,self.args["xpath_search"],to_search)
#         output.update({self.args["code"]:contents})
#         return output

# class Robot2:
#     def __init__(self, arg):
#         self.args = arg
    
#     def get_homepage(self):
#         output = {}
#         contents = []
#         content1 = get_href_title(self.args["homepage1"],self.args["homepage1"],self.args["xpath_homepage"][0:3])
#         content2 = get_href_title(self.args["homepage2"],self.args["homepage2"],self.args["xpath_homepage"][3:])
#         contents = content1 + content2
#         output.update({self.args["code"]:contents})
#         return output

#     def search_keyword(self, keyword):
#         output = {}
#         contents = []
#         code = self.args["code"]
#         print(f"{code} receiving {keyword} to search")

#         to_search = KeywordDict.search_keyword_dict(keyword, self.args["language1"])
#         if to_search==keyword:
#             translated = GoogleTranslate.translate_text([keyword],self.args["language1"])
#             to_search = translated[0]['translatedText']
#         print(f"{code} searching translated keyword: {to_search}")
        

#         keyword_string = to_search.replace(" ",self.args["search1"][1])
#         search_url = self.args["search1"][0]+keyword_string+self.args["search1"][2]
#         content1 = get_href_title(self.args["homepage1"],search_url,self.args["xpath_search"][0:3],to_search)

#         keyword_string = to_search.replace(" ",self.args["search2"][1])
#         search_url = self.args["search2"][0]+keyword_string+self.args["search2"][2]
#         content2 = get_href_title(self.args["homepage2"],search_url,self.args["xpath_search"][3:],to_search)

#         contents = content1 + content2
#         output.update({self.args["code"]:contents})
#         return output

# class Robot0:
#     def __init__(self, arg):
#         self.args = arg
    
#     def get_homepage(self):
#         output = {}
#         contents = []
#         content1 = get_href_title(self.args["homepage1"],self.args["homepage1"],self.args["xpath_homepage"][0:3])
#         content2 = get_href_title(self.args["homepage2"],self.args["homepage2"],self.args["xpath_homepage"][3:])
#         contents = content1 + content2
#         output.update({self.args["code"]:contents})
#         return output

#     def search_keyword(self, keyword):
#         output = {}
#         contents = []
#         code = self.args["code"]
#         print(f"{code} receiving {keyword} to search")

#         to_search = KeywordDict.search_keyword_dict(keyword, self.args["language1"])
#         if to_search==keyword:
#             translated = GoogleTranslate.translate_text([keyword],self.args["language1"])
#             to_search = translated[0]['translatedText']
#         print(f"{code} searching translated keyword: {to_search}")

#         keyword_string = to_search.replace(" ",self.args["search1"][1])
#         search_url = self.args["search1"][0]+keyword_string+self.args["search1"][2]
#         content1 = get_href_title(self.args["homepage1"],search_url,self.args["xpath_search"][0:3],to_search)

#         to_search = KeywordDict.search_keyword_dict(keyword, self.args["language2"])
#         if to_search==keyword:
#             translated = GoogleTranslate.translate_text([keyword],self.args["language2"])
#             to_search = translated[0]['translatedText']

#         keyword_string = to_search.replace(" ",self.args["search2"][1])
#         search_url = self.args["search2"][0]+keyword_string+self.args["search2"][2]
#         content2 = get_href_title(self.args["homepage2"],search_url,self.args["xpath_search"][3:],to_search)

#         contents = content1 + content2
#         output.update({self.args["code"]:contents})
#         return output

# class Robot3:
#     def __init__(self, arg):
#         self.args = arg
    
#     def get_homepage(self):
#         output = {}
#         contents = []
#         content1 = get_href_title(self.args["homepage1"],self.args["homepage1"],self.args["xpath_homepage"][0:2])
#         content2 = get_href_title(self.args["homepage2"],self.args["homepage2"],self.args["xpath_homepage"][2:4])
#         content3 = get_href_title(self.args["homepage3"],self.args["homepage3"],self.args["xpath_homepage"][4:])
#         contents = content1 + content2 + content3
#         output.update({self.args["code"]:contents})
#         return output

#     def search_keyword(self, keyword):
#         output = {}
#         contents = []
#         code = self.args["code"]
#         print(f"{code} receiving {keyword} to search")

#         to_search = KeywordDict.search_keyword_dict(keyword, self.args["language1"])
#         if to_search==keyword:
#             translated = GoogleTranslate.translate_text([keyword],self.args["language1"])
#             to_search = translated[0]['translatedText']
#         print(f"{code} searching translated keyword: {to_search}")

#         keyword_string = to_search.replace(" ",self.args["search1"][1])
#         search_url = self.args["search1"][0]+keyword_string+self.args["search1"][2]
#         content1 = get_href_title(self.args["homepage1"],search_url,self.args["xpath_search"][0:2],to_search)

#         keyword_string = to_search.replace(" ",self.args["search2"][1])
#         search_url = self.args["search2"][0]+keyword_string+self.args["search2"][2]
#         content2 = get_href_title(self.args["homepage2"],search_url,self.args["xpath_search"][2:4],to_search)

#         keyword_string = to_search.replace(" ",self.args["search3"][1])
#         search_url = self.args["search3"][0]+keyword_string+self.args["search3"][2]
#         content3 = get_href_title(self.args["homepage3"],search_url,self.args["xpath_search"][4:],to_search)

#         contents = content1 + content2 + content3
#         output.update({self.args["code"]:contents})
#         return output

# class HomepageGreenLand:

#     def __init__(self):
#         self.code = "GL"
#         self.language1 = "da"
#         self.homepage1 = "https://sermitsiaq.ag"
#         self.xpath_homepage = [['//*[@id="frontpage"]/section[3]/div[1]/div[1]/a','//*[@id="frontpage"]/section[3]/div[1]/div[1]/a/article/h1'],
#                                ['//*[@id="frontpage"]/section[3]/div[1]/div[2]/a[1]','//*[@id="frontpage"]/section[3]/div[1]/div[2]/a[1]/article/h1'],
#                                ['//*[@id="frontpage"]/section[3]/div[1]/div[2]/a[2]','//*[@id="frontpage"]/section[3]/div[1]/div[2]/a[2]/article/h1'],
#                                ['//*[@id="frontpage"]/section[5]/div[1]/div/a','//*[@id="frontpage"]/section[5]/div[1]/div/a/article/h1'],
#                                ['//*[@id="frontpage"]/section[7]/div[1]/a[1]','//*[@id="frontpage"]/section[7]/div[1]/a[1]/article/h1']]

#     def get_homepage(self):
#         output = {}
#         contents = []
#         contents = get_href_title(self.homepage1,self.homepage1,self.xpath_homepage)
#         output.update({self.code:contents})
#         return output

#     def search_keyword(self, keyword):
#         output = {}
#         contents = []

#         print(f"{self.code} receiving {keyword} to search")
#         translated = GoogleTranslate.translate_text([keyword],self.language1)
#         translated_keyword = translated[0]['translatedText']
#         print(f"{self.code} searching translated keyword: {translated_keyword}")

#         contents = google_search(translated_keyword, self.homepage1, 5)
        
#         output.update({self.code:contents})
#         return output


# # import time
# # time_start = time.time()
# # result = HomepageGreenLand().get_homepage()
# # time_end = time.time()
# # print("總共執行"+str(round(time_end-time_start,2))+"秒")
# # print(result)
# # homepages = result["GL"]
# # to_translate = []
# # for homepage in homepages:
# #     to_translate.append(homepage[1])
# # chinese_result = GoogleTranslate.translate_text(to_translate,"zh-TW")
# # english_result = GoogleTranslate.translate_text(to_translate,"en")
# # conn = sqlite3.connect("HOMEPAGE.db")
# # for i in range(len(to_translate)):
# #     href = homepages[i][0]
# #     original = to_translate[i]
# #     chinese = chinese_result[i]['translatedText']
# #     english = english_result[i]['translatedText']
# #     x = (href, original, chinese, english, str(datetime.now()))
# #     sql = f'''insert into GL values(?,?,?,?,?)'''
# #     conn.execute(sql, x)
# #     conn.commit()
# #     print(f'''insert into GL values = {x}''')
# # conn.close()



# import time 
# import pandas as pd 

# df = pd.read_excel("url_and_xpath.xlsx")
# df.loc[77,"code"] = "NA" 

# robots = {}
# robots.update({"GL":HomepageGreenLand()})
# for i in range(len(df)):
    
#     row = df.iloc[i,:]

#     temp_dict1 = {}
#     temp_dict1.update({"code":row["code"]})
#     temp_dict1.update({"language1":row["language1"]})
#     temp_dict1.update({"homepage1":row["homepage1"]})
#     temp_dict1.update({"xpath_homepage":[[row['xpath_homepage1_1'],row['xpath_homepage1_2']],[row['xpath_homepage2_1'],row['xpath_homepage2_2']],[row['xpath_homepage3_1'],row['xpath_homepage3_2']],[row['xpath_homepage4_1'],row['xpath_homepage4_2']],[row['xpath_homepage5_1'],row['xpath_homepage5_2']]]})
#     temp_dict1.update({"xpath_search":[[row['xpath_search1_1'],row['xpath_search1_2']],[row['xpath_search2_1'],row['xpath_search2_2']],[row['xpath_search3_1'],row['xpath_search3_2']],[row['xpath_search4_1'],row['xpath_search4_2']],[row['xpath_search5_1'],row['xpath_search5_2']]]})
    
#     spaceX = ' '
#     if row["space1"]=='PLUS':
#         spaceX = '+'
#     elif row["space1"]=='MINUS':
#         spaceX = '-'
#     searchX_2 = row["search1_2"]
#     if row["search1_2"] == 'none':
#         searchX_2 = ''
#     temp_dict1.update({"search1":[row["search1_1"],spaceX,searchX_2]})
    
#     temp_dict2 = temp_dict1
#     temp_dict2.update({"homepage2":row["homepage2"]})
#     spaceX = ' '
#     if row["space2"]=='PLUS':
#         spaceX = '+'
#     elif row["space2"]=='MINUS':
#         spaceX = '-'
#     searchX_2 = row["search2_2"]
#     if row["search2_2"] == 'none':
#         searchX_2 = ''
#     temp_dict2.update({"search2":[row["search2_1"],spaceX,searchX_2]})

#     temp_dict0 = temp_dict2
#     temp_dict0.update({"language2":row["language2"]})

#     temp_dict3 = temp_dict2
#     temp_dict3.update({"homepage3":row["homepage3"]})
#     spaceX = ' '
#     if row["space3"]=='PLUS':
#         spaceX = '+'
#     elif row["space3"]=='MINUS':
#         spaceX = '-'
#     searchX_2 = row["search3_2"]
#     if row["search3_2"] == 'none':
#         searchX_2 = ''
#     temp_dict3.update({"search3":[row["search3_1"],spaceX,searchX_2]})
    
#     if row["type"] == 0:
#         robots.update({row["code"]:Robot0(temp_dict0)})
#     elif row["type"] == 1:
#         robots.update({row["code"]:Robot1(temp_dict1)})
#     elif row["type"] == 2:
#         robots.update({row["code"]:Robot2(temp_dict2)})
#     elif row["type"] == 3:
#         robots.update({row["code"]:Robot3(temp_dict3)})

# import threading

# def print_result(code):
#     time_start = time.time()
#     result = robots[code].get_homepage("zh-TW")
#     time_end = time.time()
#     print("總共執行"+str(round(time_end-time_start,2))+"秒")
#     print(result)
#     print('')

# thread_list = []
# t1 = threading.Thread(target=print_result, args=(["JP"]))
# t2 = threading.Thread(target=print_result, args=(["TW"]))
# t3 = threading.Thread(target=print_result, args=(["CN"]))
# t4 = threading.Thread(target=print_result, args=(["KR"]))
# thread_list.append(t1)
# thread_list.append(t2)
# thread_list.append(t3)
# thread_list.append(t4)

# for t in thread_list:
#     t.start()


# time_start = time.time()
# result = robots["DK"].get_homepage()
# time_end = time.time()
# print("總共執行"+str(round(time_end-time_start,2))+"秒")
# print(result)

# homepages = result["UY"]
# to_translate = []
# for homepage in homepages:
#     to_translate.append(homepage[1])
# chinese_result = GoogleTranslate.translate_text(to_translate,"zh-TW")
# english_result = GoogleTranslate.translate_text(to_translate,"en")

# conn = sqlite3.connect("HOMEPAGE.db")
# for i in range(len(to_translate)):
#     href = homepages[i][0]
#     original = to_translate[i]
#     chinese = chinese_result[i]['translatedText']
#     english = english_result[i]['translatedText']
#     # english = to_translate[i]
#     x = (href, original, chinese, english, str(datetime.now()))
#     sql = f'''insert into UY values(?,?,?,?,?)'''
#     conn.execute(sql, x)
#     conn.commit()
#     print(f'''insert into UY values = {x}''')
# conn.close()



# import sqlite3

# conn = sqlite3.connect("HOMEPAGE.db")
# sql = f'''Create table SG(
#     href TEXT PRIMARY KEY,
#     title_original TEXT,
#     title_chinese TEXT,
#     title_english TEXT,
#     timestamp TEXT
# )'''
# conn.execute(sql)



# # 重建資料表
# conn = sqlite3.connect("HOMEPAGE.db")
# for code in robots:
#     temp = code
#     if temp == "IN":
#         temp = "INDIA"
#     if temp == "IS":
#         temp = "ICELAND"
    # sql = f'''Create table {temp}(
    #     href TEXT PRIMARY KEY,
    #     title_original TEXT,
    #     title_chinese TEXT,
    #     title_english TEXT,
    #     timestamp TEXT
    # )'''
#     conn.execute(sql)
# conn.close()

# # 新增紀錄
# conn = sqlite3.connect("HOMEPAGE.db")
# for code in robots:
#     homepages = robots[code].get_homepage()[code]
#     for homepage in homepages:
#         href = homepage[0]
#         original = homepage[1]
#         if original=='':
#             continue
#         temp_code = code
#         if temp_code=="IN":
#             temp_code = "INDIA"
#         if temp_code=="IS":
#             temp_code = "ICELAND"
#         temp = (href, original, '', '', str(datetime.now()))
#         sql = f'''insert into {temp_code} values(?,?,?,?,?)'''
#         conn.execute(sql, temp)
#         conn.commit()
#         print(f'''insert into {temp_code} values = {temp}''')
# conn.close()




# conn = sqlite3.connect("HOMEPAGE.db")
# sql = f'''SELECT * from TW where href = "https://globalnewstv.com.tw/202207/1234/"'''
# results = conn.execute(sql).fetchall()
# conn.close()


# import sqlite3

# conn = sqlite3.connect("HOMEPAGE.db")
# datedate = ('2022-08-20%',)
# sql = f'''SELECT * from US where timestamp like (?)'''
# results = conn.execute(sql,datedate).fetchall()
# conn.close()


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
browser = webdriver.Chrome()
wiki = "https://zh.wikipedia.org/wiki/"

to_search = "普丁"
browser.get(wiki+to_search)
more_language_button_xpath = '//*[@id="p-lang"]/div/ul/button'
search_language_xpath = '//*[@id="search"]/div/div/input[2]'
# WebDriverWait(browser,10).until(expected_conditions.presence_of_element_located((By.XPATH, more_language_button_xpath)))
more_language_button = browser.find_element(by=By.XPATH, value=more_language_button_xpath)
search_language = browser.find_element(by=By.XPATH, value=search_language_xpath)

import re
from types import NoneType
url_regex = "https://[a-z]+\.wikipedia\.org/wiki/"
match = re.search(url_regex, browser.current_url)
type(match)==re.Match
type(match)==NoneType


