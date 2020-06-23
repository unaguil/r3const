from direct.showbase.ShowBase import ShowBase
from panda3d.core import LPoint3f


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.models = []
        self.selectedIndex = -1
        self.model = None

        self.accept('a', self.addSphere)
        self.accept('r', self.delModel)

        self.accept('arrow_right', self.move_x_pos)
        self.accept('arrow_left', self.move_x_neg)
        self.accept('arrow_up', self.move_z_pos)
        self.accept('arrow_down', self.move_z_neg)
        self.accept('z', self.move_y_pos)
        self.accept('x', self.move_y_neg)

        self.accept('s', self.save_image)

        self.accept('t', self.exit)

        self.step = 0.1


        self.process_file('commands.txt')


    def save_image(self):
        self.movie(namePrefix='image', duration=1, fps=1, format='png')


    def addModel(self, model):
        self.models.append(model)
        self.selectedIndex = len(self.models) - 1
        self.model = self.models[self.selectedIndex]


    def addSphere(self):
        model = self.loader.loadModel("smiley.egg")
        model.reparentTo(self.render)
        model.setPos(0, 5, 0)

        self.addModel(model)


    def delModel(self):
        if self.model:
            self.model.detachNode()


    def move_x_pos(self):
        if self.model:
            pos = self.model.getPos()
            self.model.setPos(pos + LPoint3f(self.step, 0, 0))


    def move_x_neg(self):
        if self.model:
            pos = self.model.getPos()
            self.model.setPos(pos + LPoint3f(-self.step, 0, 0))


    def move_y_pos(self):
        if self.model:
            pos = self.model.getPos()
            self.model.setPos(pos + LPoint3f(0, self.step, 0))


    def move_y_neg(self):
        if self.model:
            pos = self.model.getPos()
            self.model.setPos(pos + LPoint3f(0, -self.step, 0))


    def move_z_pos(self):
        if self.model:
            pos = self.model.getPos()
            self.model.setPos(pos + LPoint3f(0, 0, self.step))


    def move_z_neg(self):
        if self.model:
            pos = self.model.getPos()
            self.model.setPos(pos + LPoint3f(0, 0, -self.step))


    def exit(self):
        self.finalizeExit()


    def process_file(self, file_path):
        with open(file_path, 'r') as input_file:
            for line in input_file:
                command = getattr(self, line.strip())
                command()

            self.save_image()



def main():
    app = MyApp()
    app.run()

if __name__ == '__main__':
    main()