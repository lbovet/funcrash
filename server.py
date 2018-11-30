from client import Client
from state import State
import time

class Server(object):
    scores = list()

    def __init__(self):
        try:
            import cred
            self.client = Client(cred.host, cred.server_username, cred.server_password)
        except ImportError:
            self.client = Client("localhost", "", "")
        self.client.subscribe("funcrash/local/score", self.score_recu)
        self.state = State()
        if self.state["scores"]:
            self.scores = self.state.scores

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
                            new_list.append(s)
                        ajoute = True
                    else:
                        new_list.append(s)
                else:
                    new_list.append(recu)
                    if s.nom != recu.nom:
                        new_list.append(s)
                    ajoute = True
            self.scores = new_list
            if len(self.scores) < 10 and not ajoute:
                self.scores.append(recu)
        self.scores = self.scores[:10]
        self.client.publish("funcrash/global/scores", self.scores, True)
        self.state.scores = self.scores

if __name__ == '__main__':
    Server()
    while True:
        time.sleep(9999999)
