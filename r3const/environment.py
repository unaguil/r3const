from panda3d.core import LVector3
from random import Random
import numpy as np
import inspect
import logging


class CommandNotFound(Exception):

    def __init__(self, message):
        super().__init__(message)


class Environment:

    def __init__(self, render, dataset, reward_func, max_actions=10, step=0.1):
        self.__render = render
        self.__dataset = dataset
        self.__reward_func = reward_func
        self.__max_actions = max_actions
        self.__step = step

        self.__random = Random()

        self.__command_ids = sorted([
            'add_sphere',
            'move_x_pos', 'move_x_neg',
            'move_y_pos', 'move_y_neg',
            'move_z_pos', 'move_z_neg',
            'finish'
        ])

        members = inspect.getmembers(Environment, predicate=inspect.isfunction)
        self.__command_funcs = {c: f  for c, f in members if c in self.__command_ids}

        self.__command_history = []

        self.__finish = False

    @property
    def render(self):
        return self.__render

    @property
    def commands(self):
        return self.__command_ids

    @property
    def last_command(self):
        return self.__command_history[-1]

    @property
    def has_model(self):
        return self.__render.get_model() is not None

    def reset(self):
        self.__command_history = []
        self.__render.reset()
        self.__image = self.__random.choice(self.__dataset)
        self.__output = self.__render.render_to_array()
        self.__finish = False
        return self.observation

    @property
    def observation(self):
        return (self.__image, self.__output)

    @property
    def original_img(self):
        return self.__image

    @property
    def render_img(self):
        return self.__output
    
    @property
    def finish(self):
        return self.__finish

    @property
    def action_space(self):
        return self.__command_ids

    @property
    def observation_space(self):
        return ((*self.__render.size, 3), (*self.__render.size, 3))

    def __execute(self, command_id):
        if command_id not in self.__command_ids:
            raise CommandNotFound(f'Unknown command "{command_id}"')

        command = self.__command_funcs[command_id]
        
        logging.debug(f'Executing command "{command_id}"')
        self.__command_history.append(command_id)
        command(self)

    def step(self, action, render=True):
        command = self.__command_ids[action]

        self.__execute(command)
        self.__output = self.__render.render_to_array()

        observation = self.observation
        reward = self.__reward_func(self)
        is_done = len(self.__command_history) == self.__max_actions or self.__finish

        return (observation, reward, is_done)

    def __translate(self, x, y, z):
        model = self.__render.get_model()
        if model:
            pos = model.getPos()
            t = LVector3(x, y, z)
            model.setPos(pos + t)


    def add_sphere(self):
        model = self.__render.loader.loadModel("smiley.egg")
        model.reparentTo(self.__render.render)
        model.setPos(0, 10, 0)
        self.__render.add_model(model)

    
    def move_x_pos(self):
        self.__translate(self.__step, 0, 0)


    def move_x_neg(self):
        self.__translate(-self.__step, 0, 0)


    def move_y_pos(self):
        self.__translate(0, self.__step, 0)


    def move_y_neg(self):
        self.__translate(0, -self.__step, 0)

    
    def move_z_pos(self):
        self.__translate(0, 0, self.__step)


    def move_z_neg(self):
        self.__translate(0, 0, -self.__step)

    def finish(self):
        self.__finish = True