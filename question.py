from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty

class Question(Popup):
    titre = StringProperty()
    question = StringProperty()
    proposition = StringProperty()
    reponse = StringProperty()
    input = ObjectProperty(rebind=True)

    def __init__(self, titre, question, proposition, longueur_max, action):
        super(Question, self).__init__()
        self.titre = titre
        self.question = question
        if(proposition):
            self.proposition = proposition
        self.action = action
        self.longueur_max = longueur_max

    def open(self):
        Popup.open(self)
        self.input.select_all()
        self.input.bind(on_text_validate=lambda _: self.ok())
        self.input.bind(text=self.check)

    def check(self, input, value):
        if value >= self.longueur_max:
            input.text = value[:self.longueur_max]

    def ok(self):
        self.action(self.reponse)
        self.dismiss()
