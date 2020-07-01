from r3const.render import Render
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    render = Render()
    render.render_file('commands.txt')