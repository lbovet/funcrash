import paho.mqtt.client as mqtt
import json
import traceback
from argparse import Namespace

class Obj(dict):
    def __getattr__(self, key):
        if not key.startswith("__"):
            return self[key]
        else:
            return object.__getattribute__(self, key)

    def __setattr__(self, key, value):
        if not key.startswith("__"):
            self[key] = value
        else:
            object.__setattr__(self, key, value)

class Client(object):

    subscriptions = dict()

    def __init__(self, host, username, password):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(username, password)
        self.client.connect(host)
        self.client.loop_start()

    def publish(self, topic, obj, retain=False):
        try:
            if not isinstance(obj, (list,)) and not isinstance(obj, (dict,)) and obj.hasattr(__dict__):
                d = obj.__dict__
            else:
                d = obj
            self.client.publish(topic, json.dumps(d), 0, retain)
        except:
            traceback.print_exc()

    def subscribe(self, topic, callback):
        try:
            self.client.subscribe(topic)
            self.subscriptions[topic] = callback
        except:
            traceback.print_exc()

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("Connected")
            for topic in self.subscriptions:
                self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        try:
            callback = self.subscriptions[msg.topic]
            if callback:
                callback(json.loads(msg.payload, object_hook=lambda d: Obj(d)))
        except:
            traceback.print_exc()
