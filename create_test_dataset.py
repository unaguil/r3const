from r3const.render import Render
from r3const.environment import Environment
from tqdm import tqdm
from PIL import Image
import h5py
import numpy as np
import sys
import random


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Expected generated dataset size')
        sys.exit(0)
    
    dataset_size = int(sys.argv[1])

    image_size = (256, 256)

    render = Render(image_size)
    env = Environment(render, None, max_actions=100)

    print(f'Generating {dataset_size} elements in dataset')

    f = h5py.File('test-dataset.hdf5', 'w')
    dataset = f.create_dataset('images', (dataset_size, *image_size, 3), dtype='i')

    model = env.render.loader.loadModel("smiley.egg")
    model.reparentTo(env.render.render)
    model.setPos(0, 10, 0)
    env.render.add_model(model)
    
    for i in tqdm(range(dataset_size)):
        invalid = True

        while invalid:
            model = env.render.get_model()

            x_random = random.randint(-2, 2)
            y_random = random.randint(0, 20)
            z_random = random.randint(-2, 2)
            
            model.setPos(x_random, y_random, z_random)

            array = env.render.render_to_array()

            if np.sum(array) > 0:
                dataset[i] = array
                invalid = False
