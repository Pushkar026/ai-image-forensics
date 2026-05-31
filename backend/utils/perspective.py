import cv2
import numpy as np
import time 

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
    start_time = time.time()

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
            "status": "insufficient_geometry",
            "lines_detected": 0,
            "vanishing_point": None,
            "consistency_score": None
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
        min_lines=1,
        max_lines_per_cluster=8
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

    intersection_start = time.time()

    dominant_clusters = cluster_lines_by_angle(
    dominant_lines,
    angle_threshold=10
)

    intersections, extended_lines = (
    get_intersections(dominant_clusters)
)



    print(
    f"Intersection Stage: "
    f"{round(time.time() - intersection_start, 2)} sec"
    )

    # ----------------------------------------
    # ANALYZE PERSPECTIVE
    # ----------------------------------------

    analysis_start = time.time()

    analysis = analyze_intersections(
    intersections
)
    if analysis.get("status") == "insufficient_geometry":

        return {
        "status": "insufficient_geometry",
        "lines_detected": len(dominant_lines),
        "vanishing_point": None,
        "consistency_score": None
    }

    print(
    f"Analysis Stage: "
    f"{round(time.time() - analysis_start, 2)} sec"
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

    draw_start = time.time()

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

    print(
    f"Drawing Stage: "
    f"{round(time.time() - draw_start, 2)} sec"
)

    cv2.imwrite(
        "results/output.jpg",
        image
    )
    
    print("\n===== DEBUG =====")
    print(f"Raw lines: {len(raw_lines)}")
    print(f"Filtered lines: {len(filtered_lines)}")
    print(f"Dominant lines: {len(dominant_lines)}")
    print(f"Intersections: {len(intersections)}")
    print(
    f"Execution Time: "
    f"{round(time.time() - start_time, 2)} sec"
)
    print("=================\n")

    return {
        "lines_detected": len(dominant_lines),
        "vanishing_point": vanishing_point,
        "consistency_score": consistency_score
    }