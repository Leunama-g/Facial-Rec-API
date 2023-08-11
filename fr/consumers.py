import json
from channels.generic.websocket import WebsocketConsumer
from fr.apis import noti
import time 


class notificationConsumer(WebsocketConsumer):
    def connect(self):
        global noti
        curr = noti[0]
        self.accept()
        while True:
            if(noti[0] > curr):
                self.send(json.dumps({"message" : "new noti"}))
                curr = noti[0]
            time.sleep(1)
    

