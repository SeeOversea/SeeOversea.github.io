import pandas as pd
keyword_dict = pd.read_excel("keyword_dictionary.xlsx")
keyword_dict.index = keyword_dict["zh-TW"]

def search_keyword_dict(keyword, language):
    if keyword in keyword_dict.index and language in keyword_dict.columns:
        print(keyword+" is in keyword dictionary")
        to_return = keyword_dict.loc[keyword, language] if type(keyword_dict.loc[keyword, language])==str else keyword
        return to_return
    else:
        return keyword