from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from r3const.commands import CommandManager
import logging


class Render(ShowBase):

    def __init__(self, size=(128, 128)):
        loadPrcFileData('', f'win-size {size[0]} {size[1]}')

        ShowBase.__init__(self, windowType='offscreen')

        self.setBackgroundColor(0, 0, 0)

        self.__models = []
        self.__selectedIndex = -1
        self.__model = None

        self.step = 0.1

    
    def get_model(self):
        return self.__model


    def add_model(self, model):
        self.__models.append(model)
        self.__selectedIndex = len(self.__models) - 1
        self.__model = self.__models[self.__selectedIndex]
    

    def remove_model(self):
        if self.__model:
            self.__model.detachNode()


    def exit(self, task):
        self.userExit()

    
    def render_to_file(self, output):
        self.graphicsEngine.renderFrame()
        self.screenshot(output, False)


    def render_file(self, commands_file, output='render.jpg'):
        logging.info(f'Rendering file "{commands_file}" to "{output}"')
        command_manager = CommandManager(render=self)
        logging.info(f'Available commands: {len(command_manager.commands)}')
        
        with open(commands_file, 'r') as input_file:
            for line in input_file:
                command = line.strip()
                command_manager.execute(command)

        self.render_to_file(output)