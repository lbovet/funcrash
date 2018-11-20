import paho.mqtt.client as mqtt
import json
from argparse import Namespace

class Client(object):

    subscriptions = dict()

    def __init__(self, username, password):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(username, password)
        self.client.connect("funcrash.chee.li")
        self.client.loop_start()

    def publish(self, topic, obj, retain=False):
        self.client.publish(topic, json.dumps(obj.__dict__), 0, retain)

    def subscribe(self, topic, callback):
        self.client.subscribe(topic)
        self.subscriptions[topic] = callback

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        for topic in self.subscriptions:
            print topic
            self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        callback = self.subscriptions[msg.topic]
        if callback:
            callback(json.loads(msg.payload, object_hook=lambda d: Namespace(**d)))
