from kivy.app import App
import pickle

class State(object):

    data = dict()
    app = None

    def __init__(self, app):
        self.app = app
        try:
            with open("./state") as file:
                self.data = pickle.load(file)
        except:
            pass

    def __setattr__(self, key, value):        
        if key not in [ "app", "data" ]:
            self.data[key] = value
            try:
                with open("./state", "w") as file:
                    pickle.dump(self.data, file)
            except:
                pass
        else:
            object.__setattr__(self, key, value)

    def __getattribute__(self, key):
        if key not in [ "app", "data" ]:
            return self.data[key]
        else:
            return object.__getattribute__(self, key)

    def __getitem__(self, key):
        if key not in [ "app", "data" ]:
            if key in self.data:
                return self.data[key]
            else:
                return None
        else:
            return object.__getattribute__(self, key)
