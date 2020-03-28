import os
import ssl
import json
import base64
import websocket
import _thread as thread
from urllib.parse import urlencode

import hmac
import hashlib

import datetime
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time


class SpeechSynthesis(object):

    # Constants used by Xunfei Open Platform
    STATUS_LAST_FRAME = 2

    MY_APPID = '5e7ebfac'
    MY_API_KEY = '906a73013f22060c7b8778699d0f5205'
    MY_API_SECRET = '1e58fde26bdc0d1054f051afb903046f'

    TEMP_WORKING_FILE = './audio/temp.pcm'

    # a static member
    wsParam = None

    def __init__(self):
        pass

    def synthesize(self, text, speed=1):
        # the intermediate working file is always temp.pcm
        if os.path.exists(SpeechSynthesis.TEMP_WORKING_FILE):
            os.remove(SpeechSynthesis.TEMP_WORKING_FILE)

        SpeechSynthesis.wsParam = WebsocketRequestParameters(Text=text, APPID=self.MY_APPID, APIKey=self.MY_API_KEY, APISecret=self.MY_API_SECRET)
        websocket.enableTrace(False)
        wsUrl = SpeechSynthesis.wsParam.create_url()
        ws = websocket.WebSocketApp(wsUrl, on_message=SpeechSynthesis.on_message, on_error=SpeechSynthesis.on_error, on_close=SpeechSynthesis.on_close)
        ws.on_open = SpeechSynthesis.on_open
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.close()

    # make sure ffmpeg is accessible from the command line. for mac, run 'brew install ffmpeg' to install
    # to convert, run a command like this --> ffmpeg -y -f s16be -ac 1 -ar 16000 -acodec pcm_s16le -i xxx.pcm xxx.mp3
    def convert_to_mp3(self, mp3_name):
        import subprocess
        p = subprocess.Popen(['ffmpeg','-y','-f','s16be','-ac','1','-ar','16000','-acodec','pcm_s16le','-i','temp.pcm',mp3_name],
                       cwd=os.getcwd()+'/audio', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        # usually stdout is used for normal message output
        # in ffmpeg, it seems that all messages are output to stderr
        # print(stdout.decode("utf-8"))
        # print(stderr.decode("utf-8"))

    def clean_up(self):
        os.remove(SpeechSynthesis.TEMP_WORKING_FILE)

    @staticmethod
    def on_open(ws):
        def run(*args):
            data = {
                    "common": SpeechSynthesis.wsParam.CommonArgs,
                    "business": SpeechSynthesis.wsParam.BusinessArgs,
                    "data": SpeechSynthesis.wsParam.Data,
                 }
            data = json.dumps(data)
            ws.send(data)

        thread.start_new_thread(run,())

    @staticmethod
    def on_error(ws, error):
        print("### websocket on_error:", ws, error)

    @staticmethod
    def on_close(ws):
        print("### websocket on_close:", ws)

    @staticmethod
    def on_message(ws, raw_message):
        try:
            # parse as json
            message = json.loads(raw_message)

            sid = message["sid"]
            code = message["code"]
            errMsg = message["message"]

            if code != 0:
                print("### websocket on_message sid",sid,"error code",code,"error message",errMsg)
                return

            status = message["data"]["status"]
            if status == SpeechSynthesis.STATUS_LAST_FRAME:
                # print("### end of data, closing websocket")
                ws.close()
                return

            raw_audio = message["data"]["audio"]
            audio = base64.b64decode(raw_audio)

            with open(SpeechSynthesis.TEMP_WORKING_FILE, 'ab') as f:
                f.write(audio)

        except Exception as e:
            print("### websocket received exception:", e)


class WebsocketRequestParameters(object):

    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # common arguments
        self.CommonArgs = {"app_id": self.APPID}

        # business related arguments (check out the official documentation for more customized configurations)
        self.BusinessArgs = {"aue": "raw",
                             "auf": "audio/L16;rate=16000",
                             # 小燕 许久 小萍 小婧 许小宝
                             # "aisjiuxu", "aisjiuxu", "aisxping", "aisjinger", "aisbabyxu",
                             "vcn": "aisxping",     # voices
                             "speed": 1,    # the slowest possible
                             "tte": "utf8"}

        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}


    def create_url(self):

        url = 'wss://tts-api.xfyun.cn/v2/tts'

        now = datetime.now()    # timestamp in RFC1123 format
        date = format_date_time(mktime(now.timetuple()))

        # prepare for the authorization challenge
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # http request parameters
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }

        # construct the final url to send to the remote server
        url = url + '?' + urlencode(v)
        # print('websocket request url :', url)

        return url
