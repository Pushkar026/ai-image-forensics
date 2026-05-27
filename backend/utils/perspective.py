import cv2
import numpy as np

def detect_lines(edges, image):

    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180,
        threshold=100,
        minLineLength=100,
        maxLineGap=10
    )

    line_count = 0

    if lines is not None:

        line_count = len(lines)

        for line in lines:

            x1, y1, x2, y2 = line[0]

            cv2.line(
                image,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

    cv2.imwrite("results/output.jpg", image)

    return line_count