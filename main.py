class Game(object):
    def __init__(self):
        self.road = Road(200)
        self.car = Car(self.road)
        self.tomatoes = list()
        self.periode = 100
        self.current_tick = 0

    def tick(self):
        self.current_tick = self.current_tick + 1
        if(self.current_tick % self.periode == 0):
            self.tomateos.add(Tomato(self.road))
        self.tomatoes = [ for t in self.tomatoes if t.x > 0]
