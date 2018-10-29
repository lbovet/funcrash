from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.logger import Logger

from road import Road
from car import Car
from tomato import Tomato

class Game(Widget):
    car = ObjectProperty(None)
    road = ObjectProperty(None)
    tomatoes = list()
    periode = 50
    current_tick = 0

    def tick(self, dt):
        self.current_tick = self.current_tick + 1
        if(self.current_tick % self.periode == 0):
            t = Tomato(self.road)
            self.tomatoes.append(t)
            self.add_widget(t)                
        for t in self.tomatoes:
            t.tick()
            if(t.x < 0):
                self.tomatoes.remove(t)
                self.remove_widget(t)
        self.car.tick()

class FuncrashApp(App):
    road = ObjectProperty(Road())

    def build(self):
        game = Game()
        Clock.schedule_interval(game.tick, 1.0 / 30.0)
        return game

if __name__ == '__main__':
    FuncrashApp().run()