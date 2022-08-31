from argparse import ArgumentParser
from collections import namedtuple

import json, time, urllib.parse, sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs
from numpy import partition
import pandas as pd

from Robot import *
import GoogleTranslate

ResponseStatus = namedtuple("HTTPStatus",
                            ["code", "message"])

ResponseData = namedtuple("ResponseData",
                          ["status", "content_type", "data_stream"])

# Mapping the output format used in the client to the content type for the
# response
CHUNK_SIZE = 1024
HTTP_STATUS = {"OK": ResponseStatus(code=200, message="OK"),
               "BAD_REQUEST": ResponseStatus(code=400, message="Bad request"),
               "NOT_FOUND": ResponseStatus(code=404, message="Not found"),
               "INTERNAL_SERVER_ERROR": ResponseStatus(code=500, message="Internal server error")}
PROTOCOL = "http"
ROUTE_INDEX = "/index.html"
ROUTE_VOICES = "/voices"
ROUTE_READ = "/read"

AVALAIBLE_LANGUAGES = ['zh-TW','en','de','fr','es','ko','ja','pt','vi','th']

################################################################

df = pd.read_excel("url_and_xpath.xlsx")
df.loc[77,"code"] = "NA" 

robots = {}
for i in range(len(df)):
    
    row = df.iloc[i,:]

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
robots["CN"] = RobotChina()

##################以上是建立機器人############################


class HTTPStatusError(Exception):
    """Exception wrapping a value from http.server.HTTPStatus"""

    def __init__(self, status, description=None):
        """
        Constructs an error instance from a tuple of
        (code, message, description), see http.server.HTTPStatus
        """
        super(HTTPStatusError, self).__init__()
        self.code = status.code
        self.message = status.message
        self.explain = description


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """An HTTP Server that handle each request in a new thread"""
    daemon_threads = True


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def processQuery(self, query):
        queryList = query.split('&')
        data = {}
        data["method"] = queryList[0].split('=')[1]
        data["countries"] = queryList[1].split('=')[1].split('%2C')
        data["user_language"] = queryList[2].split('=')[1],
        data["text"] = queryList[3].split('=')[1].split('%2B')
        return data

#######################server.py的主要負責地方在下面這一塊#####################
    def do_GET(self):
        # """Handles GET requests"""
        start_time = time.time()
        print(f"Requested by {self.client_address[0]} \n")

        # Extract values from the query string
        path, _, query_string = self.path.partition('?')
        query = self.processQuery(query_string)

        
        response = {}

        if query["method"] == 'homepage':
            conn = sqlite3.connect("HOMEPAGE.db")
            for code in query["countries"]:
                contents = []
                db_news = []
                if code == "IN":
                    db_news = conn.execute("SELECT * from INDIA").fetchall()[-5:]
                elif code == "IS":
                    db_news = conn.execute(f"SELECT * from ICELAND").fetchall()[-5:]
                else:
                    db_news = conn.execute(f"SELECT * from {code}").fetchall()[-5:]
                for news in db_news:
                    temp = {"href":news[0]}
                    temp.update({"original":news[1]})
                    for lan in AVALAIBLE_LANGUAGES:
                        temp.update({lan:""})
                    temp["zh-TW"] = news[2]
                    temp["en"] = news[3]
                    contents.append(temp)
                response.update({code:contents})
            conn.close()
        elif query["method"] == "history":
            unquotedDate = urllib.parse.unquote(query["text"][0])
            historyDate = (unquotedDate+"%",)
            conn = sqlite3.connect("HOMEPAGE.db")
            for code in query["countries"]:
                contents = []
                db_news = []
                if code == "IN":
                    sql = f'''SELECT * from INDIA where timestamp like (?)'''
                    db_news = conn.execute(sql,historyDate).fetchall()
                elif code == "IS":
                    sql = f'''SELECT * from ICELAND where timestamp like (?)'''
                    db_news = conn.execute(sql,historyDate).fetchall()
                else:
                    sql = f'''SELECT * from {code} where timestamp like (?)'''
                    db_news = conn.execute(sql,historyDate).fetchall()
                for news in db_news:
                    temp = {"href":news[0]}
                    temp.update({"original":news[1]})
                    for lan in AVALAIBLE_LANGUAGES:
                        temp.update({lan:""})
                    temp["zh-TW"] = news[2]
                    temp["en"] = news[3]
                    contents.append(temp)
                response.update({code:contents})
            conn.close()
        
        elif query["method"] == 'keyword':
            unquoted = urllib.parse.unquote(query["text"][0])
            user_language = query["user_language"] if type(query["user_language"])==str else query["user_language"][0]
            
            for code in query["countries"]:
                
                result = robots[code].search_keyword(unquoted)

                temp = result[code]
                to_translate = []
                for t in temp:
                    to_translate.append(t[1])
                translated_result = GoogleTranslate.translate_text(to_translate,user_language)
                
                out_list = []
                for i in range(len(translated_result)):
                    news_dict = {"href":temp[i][0]}
                    news_dict.update({"original":temp[i][1]})
                    for lan in AVALAIBLE_LANGUAGES:
                        news_dict.update({lan:""})
                    translated = translated_result[i]['translatedText']
                    news_dict[user_language] = translated

                    out_list.append(news_dict)

                response.update({code:out_list})
                print(response)

        
        elif query["method"] == 'translate':
            
            user_language = query["user_language"] if type(query["user_language"])==str else query["user_language"][0]

            for code in query["countries"]:

                to_translate = []
                for text in query["text"]:
                    to_translate.append(urllib.parse.unquote(text))
            
                translated_result = GoogleTranslate.translate_text(to_translate,user_language)

                out_list = []
                for result in translated_result:
                    translated = result["translatedText"]
                    out_list.append({"original":result["input"],"translated":translated})
                
                response.update({code:out_list})


        response = json.dumps(response)
        response = bytes(response, encoding='utf-8')

        try:
            response = ResponseData(status=HTTP_STATUS["OK"], content_type="application/json",data_stream=response)
            self.send_headers(response.status, response.content_type)
            self.stream_data(response.data_stream)

        except HTTPStatusError as err:
            # Respond with an error and log debug
            # information
            self.send_error(err.code, err.message, err.explain)

            self.log_error(u"%s %s %s - [%d] %s", self.client_address[0],
                           self.command, self.path, err.code, err.explain)

        end_time = time.time()
        print("本次執行"+str(round(end_time-start_time,2))+"秒")
        print("[END]")

    def send_headers(self, status, content_type):
        """Send out the group of headers for a successful request"""
        # Send HTTP headers
        self.send_response(status.code, status.message)
        self.send_header('Content-Type', content_type)
        # self.send_header('Transfer-Encoding', 'chunked')
        # self.send_header('Connection', 'close')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()

    def stream_data(self,stream):
        if stream:
            self.wfile.write(stream)               
            self.wfile.flush()

#######################################################################











# Define and parse the command line arguments
cli = ArgumentParser(description='Example Python Application')
cli.add_argument(
    "-p", "--port", type=int, metavar="PORT", dest="port", default=8000)
cli.add_argument(
    "--host", type=str, metavar="HOST", dest="host", default="localhost")
arguments = cli.parse_args()

# If the module is invoked directly, initialize the application
if __name__ == '__main__':
    # Create and configure the HTTP server instance
    server = ThreadedHTTPServer((arguments.host, arguments.port),
                                SimpleHTTPRequestHandler)
    print("Starting server, use <Ctrl-C> to stop...")

    try:
        # Listen for requests indefinitely
        server.serve_forever()
    except KeyboardInterrupt:
        # A request to terminate has been received, stop the server
        print("\nShutting down...")
        server.socket.close()
