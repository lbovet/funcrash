from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty

class Info(Popup):
    titre = StringProperty()
    text = StringProperty()

    def __init__(self, titre, text, action):
        super(Info, self).__init__()
        self.titre = titre
        self.text = text
        self.action = action

    def ok(self):
        self.dismiss()
        self.action()
