import os
import csv
import requests

API_URL = "http://127.0.0.1:8000/analyze"

results = []

for category in ["real", "ai"]:

    folder = os.path.join(
        "dataset",
        category
    )

    for filename in os.listdir(folder):

        path = os.path.join(
            folder,
            filename
        )

        with open(path, "rb") as image:

            response = requests.post(
                API_URL,
                files={
                    "file": image
                }
            )

        data = response.json()
        
        print(data)

        if data.get("consistency_score") is None:

            score = "insufficient_geometry"

        else:

            score = data.get(
        "consistency_score",
        0
    )

        results.append([
            filename,
            category,
            score
        ])

        print(
            f"{filename} -> {score}"
        )

with open(
    "results.csv",
    "w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "filename",
        "type",
        "score"
    ])

    writer.writerows(results)

print("\nDone!")