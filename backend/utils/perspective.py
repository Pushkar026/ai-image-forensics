import cv2
import numpy as np

from utils.line_filters import (
    filter_short_lines,
    cluster_lines_by_angle,
    get_dominant_clusters
)

from utils.vanishing_point import (
    get_intersections,
    analyze_intersections,
    draw_extended_lines,
    draw_intersections,
    draw_vanishing_point
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

        return {
            "lines_detected": 0,
            "vanishing_point": None,
            "consistency_score": 0
        }

    # ----------------------------------------
    # FILTER SHORT LINES
    # ----------------------------------------

    filtered_lines = filter_short_lines(
        raw_lines,
        min_length=200
    )

    # ----------------------------------------
    # CLUSTER BY ANGLE
    # ----------------------------------------

    clusters = cluster_lines_by_angle(
        filtered_lines,
        angle_threshold=10
    )

    # ----------------------------------------
    # KEEP DOMINANT CLUSTERS
    # ----------------------------------------

    dominant_lines = get_dominant_clusters(
        clusters,
        min_lines=3,
        max_lines_per_cluster=5
    )

    # ----------------------------------------
    # DRAW DOMINANT LINES
    # ----------------------------------------

    for line in dominant_lines:

        x1, y1, x2, y2 = line["coords"]

        cv2.line(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

    # ----------------------------------------
    # GET INTERSECTIONS
    # ----------------------------------------

    intersections, extended_lines = (
        get_intersections(clusters)
    )

    # ----------------------------------------
    # ANALYZE PERSPECTIVE
    # ----------------------------------------

    analysis = analyze_intersections(
        intersections
    )

    vanishing_point = analysis[
        "vanishing_point"
    ]

    consistency_score = analysis[
        "consistency_score"
    ]

    # ----------------------------------------
    # VISUALIZATION
    # ----------------------------------------

    image = draw_extended_lines(
        image,
        extended_lines
    )

    image = draw_intersections(
        image,
        intersections
    )

    image = draw_vanishing_point(
        image,
        vanishing_point,
        consistency_score
    )

    cv2.imwrite(
        "results/output.jpg",
        image
    )

    return {
        "lines_detected": len(dominant_lines),
        "vanishing_point": vanishing_point,
        "consistency_score": consistency_score
    }