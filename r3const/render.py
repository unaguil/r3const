from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
import numpy as np
import logging


class Render(ShowBase):

    def __init__(self, size=(128, 128), step=0.1):
        loadPrcFileData('', f'win-size {size[0]} {size[1]}')

        ShowBase.__init__(self, windowType='offscreen')

        self.setBackgroundColor(0, 0, 0)

        self.__models = []
        self.__selectedIndex = -1
        self.__model = None

        self.__size = size


    @property
    def size(self):
        return self.__size


    def reset(self):
        for model in self.__models:
            model.removeNode()
        
        self.__selectedIndex = -1
        self.__model = None


    def get_model(self):
        return self.__model


    def add_model(self, model):
        self.__models.append(model)
        self.__selectedIndex = len(self.__models) - 1
        self.__model = self.__models[self.__selectedIndex]
    

    def remove_model(self):
        if self.__model:
            self.__model.detachNode()

    
    def render_to_file(self, output):
        self.graphicsEngine.renderFrame()
        self.screenshot(output, False)

    
    def render_to_array(self):
        self.graphicsEngine.renderFrame()

        region = self.camNode.getDisplayRegion(0)
        texture = region.getScreenshot()
        
        data = texture.getRamImageAs('RGB')        
        array = np.frombuffer(data, np.uint8)

        array.shape = (
            texture.getXSize(), 
            texture.getYSize(), 
            3
        )

        array = array[::-1] 

        return array