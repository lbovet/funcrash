from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty

class Question(Popup):
    titre = StringProperty()
    question = StringProperty()
    proposition = StringProperty()
    reponse = StringProperty()
    input = ObjectProperty(rebind=True)    

    def __init__(self, titre, question, proposition, longueur_max, action, transform=None):
        super(Question, self).__init__(pos_hint={'top': .94})
        self.titre = titre
        self.question = question
        if(proposition):
            self.proposition = proposition
        self.action = action
        self.longueur_max = longueur_max
        self.transform = transform        

    def open(self):
        Popup.open(self)
        self.input.select_all()
        self.input.focus = True
        self.input.bind(on_text_validate=lambda _: self.ok())
        self.input.bind(text=self.check)

    def check(self, input, value):
        if len(value) >= self.longueur_max:
            input.text = value[:self.longueur_max]
        if self.transform:
            input.text = self.transform(input.text)
        return len(self.reponse.strip()) > 0

    def ok(self):
        if len(self.reponse.strip()) > 0:
            self.action(self.reponse)
            self.dismiss()
        else:
            self.input.focus = True
