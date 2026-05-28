import cv2
import numpy as np

from utils.line_filters import (
    filter_short_lines,
    cluster_lines_by_angle,
    get_dominant_clusters
)


def detect_lines(edges, image):

    raw_lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180,
        threshold=180,
        minLineLength=100,
        maxLineGap=20
    )

    if raw_lines is None:

        return 0

    # Step 1 — Remove short noisy lines
    filtered_lines = filter_short_lines(
        raw_lines,
        min_length=200
    )

    # Step 2 — Cluster lines by direction
    clusters = cluster_lines_by_angle(
        filtered_lines,
        angle_threshold=10
    )

    # Step 3 — Keep dominant directional groups
    dominant_lines = get_dominant_clusters(
        clusters,
        min_lines=3,
        max_lines_per_cluster=5
    )

    # Draw final dominant lines
    for line in dominant_lines:

        x1, y1, x2, y2 = line["coords"]

        cv2.line(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

    cv2.imwrite("results/output.jpg", image)

    return len(dominant_lines)