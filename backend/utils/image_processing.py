import cv2
import numpy as np

def decode_image(contents):

    np_arr = np.frombuffer(contents, np.uint8)

    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    return image

def resize_image(image, max_width=1600):

    height, width = image.shape[:2]

    if width <= max_width:
        return image

    scale = max_width / width

    new_width = int(width * scale)
    new_height = int(height * scale)

    resized = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA
    )

    return resized


def convert_to_gray(image):

    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def detect_edges(gray_image):

    return cv2.Canny(gray_image, 50, 150)
