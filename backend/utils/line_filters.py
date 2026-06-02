import math
from collections import defaultdict


def line_length(x1, y1, x2, y2):

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


def line_angle(x1, y1, x2, y2):

    angle = math.degrees(
        math.atan2(
            y2 - y1,
            x2 - x1
        )
    )

    return angle


def filter_short_lines(
    lines,
    min_length=80
):

    filtered = []

    for line in lines:

        x1, y1, x2, y2 = line[0]

        length = line_length(
            x1,
            y1,
            x2,
            y2
        )

        angle = line_angle(
            x1,
            y1,
            x2,
            y2
        )

        if length >= min_length:

            filtered.append({
                "coords": (
                    x1,
                    y1,
                    x2,
                    y2
                ),
                "length": length,
                "angle": angle
            })

    print(
        f"Filtered lines: {len(filtered)}"
    )

    return filtered


def cluster_lines_by_angle(
    lines,
    angle_threshold=10
):

    clusters = defaultdict(list)

    for line in lines:

        angle = line["angle"]

        cluster_key = round(
            angle / angle_threshold
        )

        clusters[cluster_key].append(
            line
        )

    print("\n===== CLUSTERS =====")

    for key, cluster in clusters.items():

        print(
            f"Cluster {key}: "
            f"{len(cluster)} lines"
        )

    print("====================\n")

    return clusters


def get_dominant_clusters(
    clusters,
    min_lines=2,
    max_lines_per_cluster=5
):

    selected_lines = []

    for cluster in clusters.values():

        if len(cluster) < min_lines:
            continue

        sorted_cluster = sorted(
            cluster,
            key=lambda line: line["length"],
            reverse=True
        )

        selected_lines.extend(
            sorted_cluster[
                :max_lines_per_cluster
            ]
        )

    print(
        f"Dominant lines selected: "
        f"{len(selected_lines)}"
    )

    return selected_lines