from panda3d.core import LVector3
import inspect
import logging


class CommandNotFound(Exception):

    def __init__(self, message):
        super().__init__(message)



class CommandManager:


    def __init__(self, render):
        self.__r = render

        members = inspect.getmembers(CommandManager, predicate=inspect.isfunction)
        self.__commands = {c: f  for c, f in members if not c.startswith('__')}


    def get_commands(self):
        return self.__commands.keys()


    def execute(self, command_name):
        if command_name not in self.__commands:
            raise CommandNotFound(f'Unknown command "{command_name}"')

        command = self.__commands[command_name]
        logging.debug(f'Executing command "{command_name}"')
        command(self)


    def __translate(self, x, y, z):
        model = self.__r.get_model()
        if model:
            pos = model.getPos()
            t = LVector3(x, y, z)
            model.setPos(pos + t)


    def add_sphere(self):
        model = self.__r.loader.loadModel("smiley.egg")
        model.reparentTo(self.__r.render)
        self.__r.add_model(model)


    def move_x_pos(self):
        self.__translate(self.__r.step, 0, 0)


    def move_x_neg(self):
        self.__translate(-self.__r.step, 0, 0)


    def move_y_pos(self):
        self.__translate(0, self.__r.step, 0)


    def move_y_neg(self):
        self.__translate(0, -self.__r.step, 0)


    def move_z_pos(self):
        self.__translate(0, 0, self.__r.step)


    def move_z_neg(self):
        self.__translate(0, 0, -self.__r.step)



