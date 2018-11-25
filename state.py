import pickle
import traceback

class State(object):

    data = dict()
    ctx = dict()

    def __init__(self, app=None):
        if app:
            from kivy.app import App
            self.ctx["data_file"] = app.user_data_dir + "/.state"
        else:
            self.ctx["data_file"] = "./.state2"
        self.ctx["local_file="] = "./.state"

        try:
            with open(self.ctx["data_file"], "rb") as f1:
                self.data = pickle.load(f1)
        except:
            try:
                with open(self.ctx["local_file="], "rb") as f2:
                    self.data = pickle.load(f2)
            except:
                traceback.print_exc()

    def __setattr__(self, key, value):
        if key not in [ "app", "data" ]:
            self.data[key] = value
            try:
                with open(self.ctx["data_file"], "wb") as f1:
                    pickle.dump(self.data, f1)
            except:
                try:
                    with open(self.ctx["local_file="], "wb") as f2:
                        pickle.dump(self.data, f2)
                except:
                    traceback.print_exc()
        else:
            object.__setattr__(self, key, value)

    def __getattribute__(self, key):
        if key not in [ "ctx", "data" ]:
            if key in self.data:
                return self.data[key]
            else:
                return None
        else:
            return object.__getattribute__(self, key)

    def __getitem__(self, key):
        if key not in [ "ctx", "data" ]:
            if key in self.data:
                return self.data[key]
            else:
                return None
        else:
            return object.__getattribute__(self, key)
