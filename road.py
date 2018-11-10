from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty

class Road(Widget):
    hauteur = NumericProperty(0)
    nb_pistes = NumericProperty(0)
    hauteur_piste = NumericProperty(0)
    longueur = NumericProperty(0)
    speed = NumericProperty(0)
