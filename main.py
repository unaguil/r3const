from r3const.render import Render
from r3const.environment import Environment
import numpy as np
import pygame
import h5py
import random
import sys


def draw_array(display, pos, array):
    array = np.swapaxes(array, 0, 1)
    surface = pygame.surfarray.make_surface(array)
    display.blit(surface, pos)


def draw_observation(display, image_size, obs):
    original_img = obs[:, :, 0:3]
    render_img = obs[:, :, 3:6]

    draw_array(display, (0, 0), original_img)
    draw_array(display, (image_size[0], 0), render_img)


def main(dataset):
    w, h, _ = dataset[0].shape
    
    pygame.init()
    display = pygame.display.set_mode((w * 2, h))

    render = Render(size=(w, h), step=0.5)
    env = Environment(render, dataset)

    obs = env.reset()    

    draw_observation(display, (w, h), obs)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            command = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    command = 'move_z_pos'
                if event.key == pygame.K_DOWN:
                    command = 'move_z_neg'
                if event.key == pygame.K_RIGHT:
                    command = 'move_x_pos'
                if event.key == pygame.K_LEFT:
                    command = 'move_x_neg'
                if event.key == pygame.K_z:
                    command = 'move_y_pos'
                if event.key == pygame.K_x:
                    command = 'move_y_neg'
                if event.key == pygame.K_s:
                    command = 'add_sphere'

                action = env.commands.index(command)
                obs, reward, done = env.step(action)

                original_img = obs[:, :, 0:3]
                render_img = obs[:, :, 3:6]
                
                draw_array(display, (0, 0), original_img)
                draw_array(display, (w, 0), render_img)


        pygame.display.flip()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error. Expected file containing dataset')
        sys.exit()

    f = h5py.File(sys.argv[1], 'r')
    dataset = f['images']

    main(dataset)