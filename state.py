from kivy.app import App
import pickle

class State(object):    

    data = dict()
    app = None

    def __init__(self, app):
        try:
            self.app = app
            with open(self.app.user_data_dir + "/state") as file:
                self.data = pickle.load(file)
        except IOError:
            pass

    def __setattr__(self, key, value):
        if key not in [ "app", "data" ]:
            self.data[key] = value
            with open(self.app.user_data_dir + "/state", "w") as file:
                pickle.dump(self.data, file)
        else:
            object.__setattr__(self, key, value)
    
    def __getattribute__(self, key):
        if key not in [ "app", "data" ]:
            return self.data[key]
        else:
            return object.__getattribute__(self, key)        