## 輸入的text如果是字串，則回傳結果為{'translatedText':'蘋果','detectedSourceLanguage':'en','input':'apple'}
## 輸入的text如果是list，則回傳結果為list，[{}, {}, {}]
def translate_text(text, tl):
    
    import six
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    to_translate = text
    if type(text)==str:
        to_translate = [text]

    ## Cloud Translate版
    from google.cloud import translate_v2
    translator = translate_v2.Client.from_service_account_json('see-oversea-test-key.json')
    result = translator.translate(to_translate, target_language=tl)
    print("Using cloud translate...")
    
    for re in result:
        re["translatedText"] = process_translated(re["translatedText"])

    return result


    # ## Selenium版
    # from selenium import webdriver
    # from selenium.webdriver.support.ui import WebDriverWait
    # from selenium.webdriver.support import expected_conditions
    # from selenium.webdriver.common.by import By
    # option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    # browser = webdriver.Chrome(options=option)
    # result = []
    # for txt in to_translate:
    #     try:
    #         send_url = "https://translate.google.com.tw?hl=zh-TW&sl=auto&tl="+tl+"&text="+txt+"&op=translate"
    #         browser.get(send_url)
    #         WebDriverWait(browser,10).until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//span[@jsname="W297wb"]')))
    #         translated = browser.find_elements(by=By.XPATH,value='//span[@jsname="W297wb"]')[0].text
    #         result.append({'translatedText':translated,'detectedSourceLanguage':'selenium','input':txt})
    #     except:
    #         result.append({'translatedText':'','detectedSourceLanguage':'selenium','input':txt})
    # browser.quit()

    # return result


def process_translated(translated):
    out = translated.replace("電暈","新冠")
    out = translated.replace("山神哲也","山上徹也")
    out = out.replace("&#39;","'")
    out = out.replace("&quot;",'"')
    out = out.replace("&lt;","〈")
    out = out.replace("&gt;","〉")
    return out