from client import Client
from state import State
import time

class Info:
    scores = None

class Server(object):
    scores = list()

    def __init__(self):
        self.client = Client("localhost", "", "")
        self.client.subscribe("funcrash/local/score", self.score_recu)
        self.state = State()
        if self.state["scores"]:
            self.scores = self.state.scores

    def score_recu(self, score_recu):
        ajoute = False
        if len(self.scores) == 0:
            self.scores.append(score_recu)
        else:
            new_list = list()
            for s in self.scores:
                if s.high_score > score_recu.high_score or ajoute:
                    if s.nom == score_recu.nom:
                        if not ajoute:
                            new_list.append(s)
                        ajoute = True
                    else:
                        new_list.append(s)
                else:
                    new_list.append(score_recu)
                    if s.nom != score_recu.nom:
                        new_list.append(s)
                    ajoute = True
            self.scores = new_list
            if len(self.scores) < 10 and not ajoute:
                self.scores.append(score_recu)
        print self.scores
        self.client.publish("funcrash/global/scores", self.scores, True)
        self.state.scores = self.scores

if __name__ == '__main__':
    Server()
    time.sleep(9999999)
