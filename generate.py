import random

from figures.Circle import Circle
from figures.Hexagon import Hexagon
from figures.Pentagon import Pentagon
from figures.Quarter import Quarter
from figures.Semicircle import Semicircle
from figures.Square import Square
from figures.Triangle import Triangle
from figures.util import get_fragment


def load_classes():
    return [
        Circle(),
        Triangle(),
        Square(),
        Pentagon(),
        Hexagon(),
        Semicircle(),
        Quarter(),
    ]


def get_figure_sample(figures, map_img):
    font_path = "./assets/RammettoOne-Regular.ttf"

    # choose random figure class
    f = random.choice(figures)

    # crop random fragment from tif
    bg = get_fragment(map_img)

    f.generate(bg)
    f.add_letter(font_path)
    f.add_reflections()
    f.add_blur()
    f.merge_with_background()

    return f.img, f.output
