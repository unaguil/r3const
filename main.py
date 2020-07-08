from r3const.render import Render
from r3const.environment import Environment
import numpy as np
import pygame
import h5py
import sys


def reward_mse(a, b):
  return -np.square(a - b).mean() / np.square(255) 


def reward_mae(a, b):
  return -np.abs(a - b).mean() / 255


def reward_iou(a, b):
  intersection = np.sum(np.logical_and(a, b))
  union = np.sum(np.logical_or(a, b))
  iou_score = intersection / union
  return iou_score


def reward_mixed(a, b):
  return reward_iou(a, b) + reward_mse(a, b)

def reward_func(env):
    if not env.has_model:
        if env.last_command.startswith('move'):
            return -1.0, False
    else:
        model = env.render.get_model()
        if not env.render.is_visible(model):
            return -1.0, True

    iou = reward_iou(env.original_img, env.render_img)
    if iou > 0.75:
        return iou * 10, True
        

    return iou, False


def draw_array(display, pos, array):
    array = np.swapaxes(array, 0, 1)
    surface = pygame.surfarray.make_surface(array)
    display.blit(surface, pos)


def draw_observation(display, image_size, obs):
    draw_array(display, (0, 0), obs[0])
    draw_array(display, (image_size[0], 0), obs[1])


def main(dataset):
    w, h, _ = dataset[0].shape
    
    pygame.init()
    display = pygame.display.set_mode((w * 2, h))

    render = Render(size=(w, h), step=0.2)
    env = Environment(render, dataset, reward_func=reward_func, max_actions=100)

    obs = env.reset()    

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

                print(f'Reward: {reward}')

                if done:
                    print('Game finished')
                    sys.exit()

        draw_observation(display, (w, h), obs)
        pygame.display.flip()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error. Expected file containing dataset')
        sys.exit()

    f = h5py.File(sys.argv[1], 'r')
    dataset = f['images']

    main(dataset)