from flask import Flask,request
import requests
import json
import configparser
inifile = configparser.SafeConfigParser()
inifile.read("./config.ini")

LINEBOT_API_EVENT ='https://trialbot-api.line.me/v1/events'
LINE_HEADERS = {
      'Content-type': 'application/json; charset=UTF-8',
          'X-Line-ChannelID':inifile.get("settings","X-Line-ChannelID"),
              'X-Line-ChannelSecret':inifile.get("settings","X-Line-ChannelSecret"),
                  'X-Line-Trusted-User-With-ACL':inifile.get("settings","X-Line-Trusted-User-With-ACL")
}

def post_event(to, content):
    msg = {
              'to': [to],
                      'toChannel': 1383378250,
                              'eventType': "138311608800106203",
                                      'content': content
                                          }
                                              proxy = {'https':inifile.get("settings","proxy")}
                                                  r = requests.post(LINEBOT_API_EVENT, 
                                                                        headers = LINE_HEADERS, 
                                                                                              data = json.dumps(msg), 
                                                                                                                    proxies=proxy)
                                                      
                                                      def post_text(to, text):
                                                          content = {
                                                                    'contentType':1,
                                                                            'toType':1,
                                                                                    'text':text,
                                                                                        }
                                                                                            post_event(to, content)


                                                                                            app = Flask(__name__)
                                                                                            @app.route("/callback", methods=['POST'])

                                                                                            def callback():
                                                                                                messages = request.json['result']    
                                                                                                    for message in messages:
                                                                                                              text = message['content']['text']
                                                                                                                      response = text
                                                                                                                              post_text(message['content']['from'], response)
                                                                                                                                  return ''

                                                                                                                                  if __name__ == "__main__":
                                                                                                                                       app.run(host = '0.0.0.0', port = 443, threaded = True, debug = True)
