import random

import cv2
import numpy as np

from figures.Figure import Figure


class Quarter(Figure):
    label = 6

    def generate(self, bg=None):
        self.init_random(bg)

        random_angle = random.choice([0, 90, 180, 270])

        self.text_scale = 0.5
        self.text_offset = (
            self.radius * 0.5 * (np.cos(np.radians(45)) + np.cos(np.radians(random_angle - 90 - 45))),
            self.radius * 0.5 * (np.sin(np.radians(45)) + np.sin(np.radians(random_angle - 90 - 45)))
        )

        cv2.ellipse(self.img, self.xy, (self.radius, self.radius), random_angle, 180, 270, self.color, -1)

        new_x = int(self.xy[0] + (0.5 * self.radius * np.sin(np.radians(random_angle))) - 0.5 * self.radius * np.cos(
            np.radians(random_angle)))
        new_y = int(self.xy[1] - (0.5 * self.radius * np.cos(np.radians(random_angle))) - 0.5 * self.radius * np.sin(
            np.radians(random_angle)))

        new_w = int(
            self.radius * np.cos(np.radians(random_angle)) + self.radius * np.sin(np.radians(random_angle)))
        new_h = int(
            self.radius * np.sin(np.radians(random_angle)) + self.radius * np.cos(np.radians(random_angle)))

        self.output = f"{self.label} {new_x / self.width} {new_y / self.width} {new_w / self.width} {new_h / self.width}"


if __name__ == "__main__":
    f = Quarter()
    f.generate()
    f.add_letter()
    f.add_reflections()
    f.add_blur()
    f.merge_with_background()

    img = f.img
    bbox = np.array(f.output.split(" "), dtype=float)[1:] * f.width

    print(bbox)

    img = cv2.rectangle(img, (int(bbox[0] - bbox[2] // 2), int(bbox[1] - bbox[3] // 2)),
                        (int(bbox[0] + bbox[2] // 2), int(bbox[1] + bbox[3] // 2)), 255, 3)

    cv2.imshow("test", f.img)
    cv2.waitKey(10000)
