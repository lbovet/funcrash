# coding: utf-8
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.logger import Logger

from road import Road
from car import Car
from tomato import Tomato
from state import State
from question import Question
from info import Info
from client import Client
import random

class Game(Widget):
    tempo = NumericProperty(0)
    car = ObjectProperty(None)
    road = ObjectProperty(None)
    src = StringProperty(None)
    score = NumericProperty(0)
    high_score = NumericProperty(0)
    best_player = StringProperty()
    tomatoes = list()
    periode_tomates_initiale = 60
    periode_accel = 300
    speed_mult = 1.1
    current_tick = -5
    pause = False
    high_scores = """
        Pour partager ton high score:
        Paramètres -> 
            Applications -> 
                Fun Crash
        Autoriser les permissions:
        - Stockage
        - Internet
    """
    score_info = None

    def __init__(self, state, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.state = state
        try:
            import cred
            self.client = Client(cred.host, cred.server_username, cred.server_password)
        except ImportError:
            self.client = Client("localhost", "", "")
        except Exception:
            pass
        try:
            self.client.subscribe("funcrash/global/scores", self.scores_recu)
        except Exception:
            pass

    def scores_recu(self, scores):
        text = ""
        for s in scores:
            text += '{: >12}'.format(s.nom)
            text += " "
            text += '{: <12}'.format(str(s.score))
            text += "\n"
        self.high_scores = text
        if self.score_info:
            self.score_info.text = text

    def start(self):
        self.score_info = None
        self.pause = False

    def reset(self):
        if self.state["high_score"]:
            self.high_score = self.state.high_score
        if self.state["nom"]:
            self.best_player = self.state.nom

        if self.score > 30:
            self.pause = True
            try:
                if self.high_score > 0:
                    self.client.publish("funcrash/local/score", dict(score=int(self.high_score), nom=self.best_player))
            except Exception as e:
                print(e)
            self.score_info = Info("High Scores", self.high_scores, self.start)
            self.score_info.open()

        self.current_tick = 2
        self.periode_tomates = self.periode_tomates_initiale * self.tempo
        self.road.speed = self.road_speed_initiale
        self.car.current_piste = 2
        self.car.bouge()
        for tom in self.tomatoes:
            self.remove_widget(tom)
        self.tomatoes = list()
        no_car = random.randint(1,6)
        self.car.children[0].source ="images/car0"+str(no_car)+".png"

    def ajoute_tomate(self):
        t = Tomato(self.road)
        self.tomatoes.append(t)
        self.add_widget(t)

    def tick(self, dt):
        if(self.pause):
            return
        self.current_tick = self.current_tick + 1
        if(self.current_tick < 1):
            return

        if(self.current_tick == 1):
            self.road_speed_initiale = self.road.speed
            self.reset()

        self.score = str(self.current_tick)
        if(self.score > self.high_score):
            self.high_score = self.score

        # Ajoute une tomate à chaque "période tomate"
        if(self.current_tick % self.periode_tomates == 0):
            self.ajoute_tomate()
            self.ajoute_tomate()

        # Modifie la vitesse de la route à chaque "période accel"
        if(self.current_tick % self.periode_accel == 0):
            self.road.speed = self.road.speed * self.speed_mult
            self.periode_tomates = round(self.periode_tomates / self.speed_mult)

        # Pour chaque tomate...
        for t in self.tomatoes:
            t.tick()

            # Enlève la tomate si elle est tout à gauche
            if(t.x < -self.road.longueur):
                self.tomatoes.remove(t)
                self.remove_widget(t)

            # Réinitialise en cas de collision
            if t.collide_widget(self.car):
                if not self.state.high_score or self.high_score > self.state.high_score:
                    self.state.high_score = self.high_score
                    self.pause = True                    
                    q = Question("Nom du joueur", "Quel est ton nom?", self.state.nom, 12, self.enregistre_nom, self.transform)
                    q.open()
                else:
                    self.reset()
                break

    def transform(self, s):
        return s.strip().upper()

    def enregistre_nom(self, nom):
        self.pause = False
        self.best_player = nom
        self.state.nom = nom
        self.reset()

    def on_touch_down(self, touch):
        if touch.y > self.height / 2:
            self.car.up()
        else:
            self.car.down()

class FuncrashApp(App):
    road = ObjectProperty(Road())

    def build(self):
        game = Game(State(self))
        Clock.schedule_interval(game.tick, 1.0 / 30.0)
        return game

if __name__ == '__main__':
    FuncrashApp().run()
