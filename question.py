from kivy.uix.popup import Popup
from kivy.properties import StringProperty

class Question(Popup):
    titre = StringProperty()
    question = StringProperty()
    proposition = StringProperty()
    reponse = StringProperty()

    def __init__(self, titre, question, proposition, action):
        super(Question, self).__init__()
        self.titre = titre
        self.question = question
        if(proposition):
            self.proposition = proposition
        self.action = action

    def ok(self):
        self.action(self.reponse)
        self.dismiss()
