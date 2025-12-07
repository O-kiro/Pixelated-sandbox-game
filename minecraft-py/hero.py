key_switch_mode = 'z'
key_switch_camera = 'c'


key_forward = 'w'
key_back = 's'
key_left = 'a'
key_right = 'd'
key_up = 'e'
key_down = 'q'

key_turn_left = 'g'
key_turn_right = 'f'

key_build = 'mouse1'
key_destroy = 'mouse3'

key_savemap = 'k'
key_loadmap = 'l'

class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.mode = True
        self.cameraOn = True

        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)

        self.bindCamera()
        self.acceptEvents()

    # ---------------- CAMERA ----------------
    def bindCamera(self):
        base.disableMouse()
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        base.camera.setH(180)
        self.cameraOn = True

    def freeCamera(self):
        pos = self.hero.getPos()
        base.camera.reparentTo(render)
        base.camera.setPos(pos + (0, -15, 10))
        base.camera.lookAt(self.hero)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        self.freeCamera() if self.cameraOn else self.bindCamera()

    # ---------------- MOVEMENT CORE ----------------
    def check_dir(self, angle):
        dirs = [
            ((337, 360), (0, -1)),
            ((0, 22),   (0, -1)),
            ((23, 67),  (1, -1)),
            ((68, 112), (1, 0)),
            ((113, 157), (1, 1)),
            ((158, 202), (0, 1)),
            ((203, 247), (-1, 1)),
            ((248, 292), (-1, 0)),
            ((293, 336), (-1, -1)),
        ]
        for (a, b), vec in dirs:
            if a <= angle <= b:
                return vec
        return (0, -1)

    def look_at(self, angle):
        x, y, z = self.hero.getPos()
        dx, dy = self.check_dir(angle)
        return (round(x + dx), round(y + dy), round(z))

    # ---------------- MOVEMENT ACTIONS ----------------
    def move_to(self, angle):
        if self.mode:
            self.hero.setPos(self.look_at(angle))
        else:
            self.try_move(angle)

    def try_move(self, angle):
        pos = self.look_at(angle)

        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            up = (pos[0], pos[1], pos[2] + 1)
            if self.land.isEmpty(up):
                self.hero.setPos(up)

    def forward(self):
        self.move_to(self.hero.getH() % 360)

    def back(self):
        self.move_to((self.hero.getH() + 180) % 360)

    def left(self):
        self.move_to((self.hero.getH() + 90) % 360)

    def right(self):
        self.move_to((self.hero.getH() + 270) % 360)

    # ---------------- BUILD / DESTROY ----------------
    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        (self.land.addBlock if self.mode else self.land.buildBlock)(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        (self.land.delBlock if self.mode else self.land.delBlockFrom)(pos)

    # ---------------- OTHER ----------------
    def changeMode(self):
        self.mode = not self.mode #ubah mode ke True atau False
        print("switching mode:", self.mode) #print mode di terminal

    def turn_left(self):
        self.hero.setH(self.hero.getH() + 5)

    def turn_right(self):
        self.hero.setH(self.hero.getH() - 5)
#up dan down akan berjalan jika mode sedang dalam kondisi True
    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

    # ---------------- KEY EVENTS ----------------
    def acceptEvents(self):
        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)

        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)

        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)

        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)

        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)

        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)

        base.accept(key_switch_camera, self.changeView)
        base.accept(key_switch_mode, self.changeMode)

        base.accept(key_up, self.up)
        base.accept(key_up + '-repeat', self.up)

        base.accept(key_down, self.down)
        base.accept(key_down + '-repeat', self.down)

        base.accept(key_build, self.build)
        base.accept(key_destroy, self.destroy)

        base.accept(key_savemap, self.land.saveMap)
        base.accept(key_loadmap, self.land.loadMap)