from r3const.render import Render
import matplotlib.pyplot as plt
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    render = Render()
    
    render.reset()
    render.execute_file('commands.txt')

    array = render.render_to_array()

    plt.imshow(array)
    plt.show()