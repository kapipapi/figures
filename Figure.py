import random
import uuid
from os import path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class Figure:
    text_scale = 1.0
    text_angle_offset = 0
    text_offset = (0, 0)

    def __init__(self):
        self.width = 640

        # image variable
        self.img = None

        # image background
        self.bg = None

        # figure color
        self.color = None

        # figure parameters
        self.xy = None
        self.radius = None

        self.output = None

    def init_random(self, bg_img):
        self.output: str = ""

        self.img = np.zeros((self.width, self.width, 4), dtype=np.uint8)

        if bg_img is None:
            self.bg = np.zeros((self.width, self.width, 3), np.uint8)
            bg_c = np.random.randint(255, size=3)
            cv2.rectangle(self.bg, (0, 0), (self.width, self.width), (int(bg_c[0]), int(bg_c[1]), int(bg_c[2])), -1)
        else:
            self.bg = bg_img

        self.radius = np.random.randint(64, self.width / 2, size=1)[0]
        self.xy = np.random.randint(self.radius, self.width - self.radius, size=2)

        c = np.random.randint(255, size=3)
        self.color = (int(c[0]), int(c[1]), int(c[2]), 255)

    def add_letter(self, font_path):
        font = ImageFont.truetype(font_path, int(self.radius * self.text_scale))
        letter = random.choice(["A", "B", "C"])

        image = Image.fromarray(self.img)
        draw = ImageDraw.Draw(image)
        draw.text(self.xy - (self.radius * 0.5, self.radius * 0.85) + self.text_offset, letter, font=font,
                  fill=(255, 255, 255),
                  align="center")

        self.img = np.array(image)

    def add_reflections(self):
        reflections = np.zeros((self.width, self.width), dtype=np.uint8) + 100

        r = np.random.randint(100, self.width / 4, size=1)[0]
        xy = np.random.randint(r, self.width - r, size=2)

        reflections = cv2.circle(reflections, xy, r, 255, -1)
        reflections = cv2.GaussianBlur(reflections, (r * 2 + 1, r * 2 + 1), 1000) / 255

        for c in range(0, 3):
            self.img[:, :, c] = np.array(reflections * self.img[:, :, c], dtype=np.uint8)

    def add_blur(self):
        self.img = cv2.GaussianBlur(self.img, (5, 5), 5)

    def merge_with_background(self):
        assert self.img is not None
        assert self.bg is not None

        mask = self.img[:, :, 3] / 255
        inverted = 1 - mask

        output = np.zeros((self.width, self.width, 3), dtype=np.uint8)

        for c in range(0, 3):
            output[:, :, c] = np.array(((mask * self.img[:, :, c]) + (inverted * self.bg[:, :, c])), dtype=np.uint8)

        self.img = output

    def save(self, destination):
        unique_id = str(uuid.uuid1())

        im = Image.fromarray(self.img)

        im.save(path.join("generated", destination, unique_id + '.png'), quality=100, format='png')

        with open(path.join("generated", destination, unique_id + '.txt'), 'w') as f:
            f.write(self.output)
            f.close()

    def get_shape_coordinates(self, number_of_vertices, angle_rotation=0):
        coordinates = []
        for vertex in range(number_of_vertices):
            coordinates.append(
                (
                    self.radius * np.cos(2 * np.pi * vertex / number_of_vertices) + self.xy[0],
                    self.radius * np.sin(2 * np.pi * vertex / number_of_vertices) + self.xy[1]
                )
            )

        r_coordinates = []
        for item in coordinates:
            r_coordinates.append(
                (
                    (item[0] - self.xy[0]) * np.cos(angle_rotation) -
                    (item[1] - self.xy[1]) * np.sin(angle_rotation) + self.xy[0],

                    (item[0] - self.xy[0]) * np.sin(angle_rotation) +
                    (item[1] - self.xy[1]) * np.cos(angle_rotation) + self.xy[1]
                )
            )

        r_coordinates = [(int(item[0]), int(item[1])) for item in r_coordinates]

        return r_coordinates
