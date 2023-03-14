import cv2
import numpy as np


def load_map(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    print(f'{path}, dtype: {img.dtype}, shape: {img.shape}, min: {np.min(img)}, max: {np.max(img)}')

    assert np.min(img) == 0 and np.max(img) == 255

    return img


def get_fragment(img, window_size=640):
    h, w, _ = img.shape

    # window size scaled
    scale = np.random.randint(1, 3, 1)[0]
    wss = int(window_size * scale)

    x = np.random.randint(0, w - wss, 1)[0]
    y = np.random.randint(0, h - wss, 1)[0]

    output = img[y:y + wss, x:x + wss]

    return cv2.resize(output, (window_size, window_size))


if __name__ == "__main__":
    map_img = load_map("./assets/suasorto.tif")
    for _ in range(100):
        fragment = get_fragment(map_img)
        cv2.imshow("fragment", fragment)
        cv2.waitKey(5000)
