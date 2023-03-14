import cv2
import numpy as np

from figures.Figure import Figure


class Square(Figure):
    label = 2

    def generate(self, bg: None):
        self.init_random(bg)

        coords = np.array(self.get_shape_coordinates(4, np.random.randint(360, size=1)[0]))

        cv2.drawContours(self.img, [coords], 0, self.color, -1)

        x, y, w, h = cv2.boundingRect(coords)

        self.output = f"{self.label} {(x + w / 2) / self.width} {(y + h / 2) / self.width} {(w) / self.width} {(h) / self.width}"
