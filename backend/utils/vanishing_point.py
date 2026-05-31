import cv2
import numpy as np
from sklearn.cluster import DBSCAN


def extend_line(x1, y1, x2, y2, length=5000):

    dx = x2 - x1
    dy = y2 - y1

    norm = np.sqrt(dx**2 + dy**2)

    if norm == 0:
        return None

    dx /= norm
    dy /= norm

    x1_extended = int(x1 - dx * length)
    y1_extended = int(y1 - dy * length)

    x2_extended = int(x2 + dx * length)
    y2_extended = int(y2 + dy * length)

    return (
        x1_extended,
        y1_extended,
        x2_extended,
        y2_extended
    )


def line_intersection(line1, line2):

    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    denominator = (
        (x1 - x2) * (y3 - y4)
        - (y1 - y2) * (x3 - x4)
    )

    if abs(denominator) < 1e-6:
        return None

    px = (
        ((x1 * y2 - y1 * x2) * (x3 - x4))
        - ((x1 - x2) * (x3 * y4 - y3 * x4))
    ) / denominator

    py = (
        ((x1 * y2 - y1 * x2) * (y3 - y4))
        - ((y1 - y2) * (x3 * y4 - y3 * x4))
    ) / denominator

    return (int(px), int(py))


def get_intersections(clusters):

    intersections = []

    extended_lines = []

    cluster_keys = list(clusters.keys())

    # ------------------------------------------------
    # EXTEND ALL LINES
    # ------------------------------------------------

    extended_cluster_lines = {}

    for key, lines in clusters.items():

        extended_cluster_lines[key] = []

        for line in lines:

            x1, y1, x2, y2 = line["coords"]

            extended = extend_line(
                x1,
                y1,
                x2,
                y2
            )

            if extended is not None:

                extended_cluster_lines[key].append(
                    extended
                )

                extended_lines.append(extended)

    # ------------------------------------------------
    # INTERSECT ONLY DIFFERENT ANGLE CLUSTERS
    # ------------------------------------------------

    for i in range(len(cluster_keys)):

        for j in range(i + 1, len(cluster_keys)):

            cluster1 = extended_cluster_lines[
                cluster_keys[i]
            ]

            cluster2 = extended_cluster_lines[
                cluster_keys[j]
            ]

            for line1 in cluster1:

                for line2 in cluster2:

                    point = line_intersection(
                        line1,
                        line2
                    )

                    if point is not None:

                        px, py = point

                        if (
                            -10000 < px < 10000
                            and
                            -10000 < py < 10000
                        ):

                            intersections.append(point)
    total_lines = 0

    for lines in clusters.values():
        total_lines += len(lines)

    print(f"Lines used for intersections: {total_lines}")

    return intersections, extended_lines


def analyze_intersections(intersections):

    if len(intersections) == 0:

        return {
            "status": "insufficient_geometry",
            "vanishing_point": None,
            "consistency_score": None,
            "cluster_ratio": 0
        }

    points = np.array(intersections)

    print(
        f"Points before compression: {len(points)}"
    )

    # ----------------------------------------
    # COMPRESS NEAR-DUPLICATE POINTS
    # ----------------------------------------

    points = np.round(
        points / 5
    ) * 5

    points = np.unique(
        points,
        axis=0
    )

    print(
        f"Points after compression: {len(points)}"
    )

    # ----------------------------------------
    # DBSCAN
    # ----------------------------------------

    clustering = DBSCAN(
        eps=80,
        min_samples=4
    ).fit(points)

    labels = clustering.labels_

    unique_labels = set(labels)

    best_cluster = []
    best_size = 0

    for label in unique_labels:

        if label == -1:
            continue

        cluster_points = points[labels == label]

        if len(cluster_points) > best_size:

            best_size = len(cluster_points)
            best_cluster = cluster_points

    if len(best_cluster) == 0:

        return {
            "status": "insufficient_geometry",
            "vanishing_point": None,
            "consistency_score": None,
            "cluster_ratio": 0
        }

    vanishing_point = np.mean(
        best_cluster,
        axis=0
    )

    # ----------------------------------------
    # FORENSIC METRICS
    # ----------------------------------------

    total_intersections = len(points)

    cluster_ratio = (
        len(best_cluster)
        / total_intersections
    )

    distances = []

    for point in best_cluster:

        distance = np.linalg.norm(
            point - vanishing_point
        )

        distances.append(distance)

    spread = np.mean(distances)

    spread_penalty = min(
        spread / 300,
        1
    )

    consistency_score = (
        cluster_ratio
        * (1 - spread_penalty)
    )

    return {
        "vanishing_point": (
            int(vanishing_point[0]),
            int(vanishing_point[1])
        ),
        "consistency_score": round(
            consistency_score,
            3
        ),
        "cluster_ratio": round(
            cluster_ratio,
            3
        )
    }


def draw_extended_lines(image, extended_lines):

    for line in extended_lines:

        x1, y1, x2, y2 = line

        cv2.line(
            image,
            (x1, y1),
            (x2, y2),
            (255, 255, 0),
            1
        )

    return image


def draw_intersections(image, intersections):

    for point in intersections:

        cv2.circle(
            image,
            point,
            3,
            (255, 0, 0),
            -1
        )

    return image


def draw_vanishing_point(
    image,
    vanishing_point,
    consistency_score
):

    if vanishing_point is None:
        return image

    cv2.circle(
        image,
        vanishing_point,
        15,
        (0, 0, 255),
        -1
    )

    text = (
        f"Consistency: {consistency_score}"
    )

    cv2.putText(
        image,
        text,
        (
            vanishing_point[0] + 20,
            vanishing_point[1]
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    return image