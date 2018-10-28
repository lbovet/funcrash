import random

class Tomato(object):
    def __init__(self, road):
        self.piste = random.randint(0, 4)
        self.x = road.longueur
        self.y = road.hauteur_piste * self.piste
        self.speed = 10

    def tick(self):
        self.x = self.x - self.speed
