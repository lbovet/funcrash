class Road(object):
    def __init__(self, h):
        self.hauteur_piste = h

class Car(object):

    def __init__(self, road):
        self.largeur = 100
        self.hauteur = 60
        self.current_piste = 2
        self.x = self.largeur/2
        self.calcule_position(road)

    def calcule_position(self, road):
        self.y = road.hauteur_piste * self.current_piste

    def up(self, road):
        if(self.current_piste < 4):
            self.current_piste = self.current_piste + 1
            self.calcule_position(road)

    def down(self, road):
        if(self.current_piste > 0):
            self.current_piste = self.current_piste - 1
            self.calcule_position(road)

#######

r = Road(200)
c = Car(r)

print(c.y)
c.up(r)
print(c.y)
c.down(r)
print(c.y)
c.up(r)
print(c.y)
c.up(r)
print(c.y)
c.up(r)
print(c.y)
c.down(r)
print(c.y)
c.down(r)
print(c.y)
c.down(r)
print(c.y)
c.down(r)
print(c.y)
c.down(r)
print(c.y)
