import cv2

from figures.Figure import Figure


class Circle(Figure):
    label = 0

    def generate(self, bg=None):
        self.init_random(bg)

        cv2.circle(self.img, self.xy, self.radius, self.color, -1)

        self.output = f"{self.label} {self.xy[0] / self.width} {self.xy[1] / self.width} {2 * self.radius / self.width} {2 * self.radius / self.width}"
