from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.logger import Logger
import random

class Tomato(Widget):
    road = ObjectProperty(rebind=True)
    x = NumericProperty(0)
    y = NumericProperty(0)
    height = NumericProperty(0)

    def __init__(self, road):
        self.road = road
        super(Tomato, self).__init__()
        self.piste = random.randint(0, 4)
        self.x = self.road.longueur
        self.y = self.road.hauteur_piste * self.piste + (self.road.hauteur_piste - self.height) / 2
                   

    def tick(self):
        self.x = self.x - self.road.speed
