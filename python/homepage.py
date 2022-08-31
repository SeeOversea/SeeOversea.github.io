import pandas as pd
import time, sqlite3
from datetime import datetime
import GoogleTranslate
from Robot import *

df = pd.read_excel("url_and_xpath.xlsx")
df.loc[77,"code"] = "NA"

# # 重建資料表
# conn = sqlite3.connect("HOMEPAGE.db")
# for code in robots:
#     temp = code
#     if temp == "IN":
#         temp = "INDIA"
#     if temp == "IS":
#         temp = "ICELAND"
#     sql = f'''Create table {temp}(
#         href TEXT PRIMARY KEY,
#         title_original TEXT,
#         title_chinese TEXT,
#         title_english TEXT,
#         timestamp TEXT
#     )'''
#     conn.execute(sql)
# conn.close()


def update_database(country_df):

    robots = {}

    ## 建立機器人
    for i in range(len(country_df)):
        row = country_df.iloc[i,:]

        temp_dict1 = {}
        temp_dict1.update({"code":row["code"]})
        temp_dict1.update({"language1":row["language1"]})
        temp_dict1.update({"homepage1":row["homepage1"]})
        temp_dict1.update({"xpath_homepage":[[row['xpath_homepage1_1'],row['xpath_homepage1_2']],[row['xpath_homepage2_1'],row['xpath_homepage2_2']],[row['xpath_homepage3_1'],row['xpath_homepage3_2']],[row['xpath_homepage4_1'],row['xpath_homepage4_2']],[row['xpath_homepage5_1'],row['xpath_homepage5_2']]]})
        temp_dict1.update({"xpath_search":[[row['xpath_search1_1'],row['xpath_search1_2']],[row['xpath_search2_1'],row['xpath_search2_2']],[row['xpath_search3_1'],row['xpath_search3_2']],[row['xpath_search4_1'],row['xpath_search4_2']],[row['xpath_search5_1'],row['xpath_search5_2']]]})
        
        spaceX = ' '
        if row["space1"]=='PLUS':
            spaceX = '+'
        elif row["space1"]=='MINUS':
            spaceX = '-'
        searchX_2 = row["search1_2"]
        if row["search1_2"] == 'none':
            searchX_2 = ''
        temp_dict1.update({"search1":[row["search1_1"],spaceX,searchX_2]})
        
        temp_dict2 = temp_dict1
        temp_dict2.update({"homepage2":row["homepage2"]})
        spaceX = ' '
        if row["space2"]=='PLUS':
            spaceX = '+'
        elif row["space2"]=='MINUS':
            spaceX = '-'
        searchX_2 = row["search2_2"]
        if row["search2_2"] == 'none':
            searchX_2 = ''
        temp_dict2.update({"search2":[row["search2_1"],spaceX,searchX_2]})

        temp_dict0 = temp_dict2
        temp_dict0.update({"language2":row["language2"]})

        temp_dict3 = temp_dict2
        temp_dict3.update({"homepage3":row["homepage3"]})
        spaceX = ' '
        if row["space3"]=='PLUS':
            spaceX = '+'
        elif row["space3"]=='MINUS':
            spaceX = '-'
        searchX_2 = row["search3_2"]
        if row["search3_2"] == 'none':
            searchX_2 = ''
        temp_dict3.update({"search3":[row["search3_1"],spaceX,searchX_2]})
        
        if row["type"] == 0:
            robots.update({row["code"]:Robot0(temp_dict0)})
        elif row["type"] == 1:
            robots.update({row["code"]:Robot1(temp_dict1)})
        elif row["type"] == 2:
            robots.update({row["code"]:Robot2(temp_dict2)})
        elif row["type"] == 3:
            robots.update({row["code"]:Robot3(temp_dict3)})
    
    robots.update({"GL":HomepageGreenLand()})
    ##################################################################################


    ## 開始新增紀錄
    conn = sqlite3.connect("HOMEPAGE.db")
    with open("更新資料庫紀錄檔.txt","a",encoding="UTF-8") as log:
        for code in robots:
            try:
                print(f"Now processing {code} ... time: {str(datetime.now())}")
                log.write(f"Now processing {code} ... time: {str(datetime.now())}\n")
                time_start = time.time()
                result = robots[code].get_homepage()
                time_end = time.time()
                print("總共執行"+str(round(time_end-time_start,2))+"秒")
                log.write("總共執行"+str(round(time_end-time_start,2))+"秒\n")
                print(result)
                log.write(str(result)+"\n")

                homepages = robots[code].get_homepage()[code]
                
                temp_code = code
                if code=="IN":
                    temp_code = "INDIA"
                elif code=="IS":
                    temp_code = "ICELAND"
                
                for homepage in homepages:
                    href = homepage[0]
                    original = homepage[1]
                    if href=='':
                        continue
                    if original=='':
                        continue

                    sql = f'''SELECT * from {temp_code} where href = (?)'''
                    search = conn.execute(sql, (str(href),)).fetchall()
                    if len(search)>0:
                        print("news exists in db")
                        log.write("news exists in db\n")
                        continue
                    
                    
                    chinese = GoogleTranslate.translate_text([original], "zh-TW")[0]['translatedText']
                    print("Successfully translate to Chinese")
                    log.write("Successfully translate to Chinese\n")

                    english = GoogleTranslate.translate_text([original], "en")[0]['translatedText']
                    print("Successfully translate to English")
                    log.write("Successfully translate to English\n")
                    
                    temp = (href, original, chinese, english, str(datetime.now()))
                    sql = f'''insert into {temp_code} values(?,?,?,?,?)'''
                    conn.execute(sql, temp)
                    conn.commit()
                    print(f'''insert into {temp_code} values = {temp}''')
                    log.write(f'''insert into {temp_code} values = {temp}\n''')
                    print('')
                    log.write("\n")

            except Exception as e:
                print("Unknown Error:" + str(e))
                log.write("Unknown Error:" + str(e) + "\n")
                print('')
                log.write("\n")
                continue
    conn.close()

import sys
if __name__ == '__main__':
    if len(sys.argv)==1:
        print("Usage: python homepage.py all")
        print("   or: python homepage.py range x y")
    elif sys.argv[1] == "all":
        update_database(df)
    elif sys.argv[1] == "range":
        start = int(sys.argv[2])
        end = int(sys.argv[3])
        update_database(df[start:end])
    else:
        print("Usage: python homepage.py all")
        print("   or: python homepage.py range x y")



# if __name__ == '__main__':

#     print("Start updating homepage...:")

#     while True:
#         try:
            


#             # 每15分鐘更新一次
#             time.sleep(60*15)
#         except KeyboardInterrupt:
#             print("\nShutting down...")
#             ###########################
#             #      中斷資料庫連線      #
#             ###########################
#             conn.close()
#             break
