from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty

class Info(Popup):
    titre = StringProperty()
    text = StringProperty()

    def __init__(self, titre, text, action):
        super(Info, self).__init__()
        self.titre = titre
        self.text = text
        self.action = action
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if self.button.focus and keycode == 40:
            self.ok()

    def ok(self):
        Window.unbind(on_key_down=self.on_key_down)
        self.dismiss()
        self.action()
