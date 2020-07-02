from r3const.render import Render
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

    image_size = (64, 64)

    render = Render(image_size)

    print(f'Generating {dataset_size} elements in dataset')

    f = h5py.File('test-dataset.hdf5', 'w')
    dataset = f.create_dataset('images', (dataset_size, *image_size, 3), dtype='i')

    render.execute('add_sphere')
    for i in tqdm(range(dataset_size)):
        model = render.get_model()

        x_random = random.randint(-2, 2)
        y_random = random.randint(0, 50)
        z_random = random.randint(-2, 2)
        
        model.setPos(x_random, y_random, z_random)

        array = render.render_to_array()

        dataset[i] = array