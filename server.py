from client import Client
from state import State
import time

class Server(object):
    scores = list()
    blacklist = list()

    def __init__(self):
        try:
            import cred
            self.client = Client(cred.host, cred.server_username, cred.server_password)
        except ImportError:
            self.client = Client("localhost", "", "")
        self.client.subscribe("funcrash/local/score", self.score_recu)
        self.client.subscribe("funcrash/global/censor", self.censor)
        self.state = State()
        if self.state["scores"]:
            self.scores = self.state.scores
        if self.state["blacklist"]:
            self.blacklist = self.state.blacklist

    def censor(self, s):
        self.blacklist.append(s.nom)

    def add(self, l, s):
        if s.nom not in self.blacklist:
            l.append(s)

    def score_recu(self, recu):
        ajoute = False
        if len(self.scores) == 0:
            self.scores.append(recu)
        else:
            new_list = list()
            for s in self.scores:
                if s.score > recu.score or ajoute:
                    if s.nom == recu.nom:
                        if not ajoute:
                            self.add(new_list, s)
                        ajoute = True
                    else:
                        self.add(new_list, s)
                else:
                    self.add(new_list, recu)
                    if s.nom != recu.nom:
                        self.add(new_list, s)
                    ajoute = True
            self.scores = new_list
            if len(self.scores) < 10 and not ajoute:
                self.add(self.scores, recu)
        self.scores = self.scores[:10]
        self.client.publish("funcrash/global/scores", self.scores, True)
        self.state.scores = self.scores

if __name__ == '__main__':
    Server()
    while True:
        time.sleep(9999999)
