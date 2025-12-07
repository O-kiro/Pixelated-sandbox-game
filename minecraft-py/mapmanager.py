import pickle

class MapManager():
    def __init__(self):
        self.model = 'block'
        self.texture = 'brick.png'
        self.startNew()
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.7, 0.2, 0.2, 1),
            (0.5, 0.3, 0.0, 1)
        ]

    def getColor(self, z):
        return self.colors[z] if z < len(self.colors) else self.colors[-1]

    def startNew(self):
        self.land = render.attachNewNode("Land")

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def addBlock(self, pos):
        x, y, z = pos
        block = loader.loadModel(self.model)
        block.setTexture(loader.loadTexture(self.texture))
        block.setPos(pos)
        block.setColor(self.getColor(z))
        block.setTag("at", f"{x},{y},{z}")   # IMPORTANT FIX
        block.reparentTo(self.land)

    def findBlocks(self, pos):
        x, y, z = pos
        return self.land.findAllMatches(f"**/=at={x},{y},{z}")  # FIXED QUERY

    def isEmpty(self, pos):
        return len(self.findBlocks(pos)) == 0

    def findHighestEmpty(self, pos):
        x, y, z = pos
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def buildBlock(self, pos):
        x, y, z = pos
        new_pos = self.findHighestEmpty((x, y, z))
        if new_pos[2] <= z + 1:     # allow placing only near surface
            self.addBlock(new_pos)

    def delBlock(self, pos):
        for b in self.findBlocks(pos):
            b.removeNode()

    def delBlockFrom(self, pos):
        x, y, z = self.findHighestEmpty(pos)
        target = (x, y, z - 1)
        for b in self.findBlocks(target):
            b.removeNode()

    def loadLand(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                for z in line.split():
                    height = int(z)
                    for h in range(height + 1):
                        self.addBlock((x, y, h))
                    x += 1
                y += 1
        return x, y

    def saveMap(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)

    def loadMap(self):
        self.clear()
        with open('my_map.dat', 'rb') as fin:
            length = pickle.load(fin)
            for i in range(length):
                pos = pickle.load(fin)
                self.addBlock(pos)
