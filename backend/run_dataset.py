import os
import csv
import requests

API_URL = "http://127.0.0.1:8000/analyze"

results = []

for category in ["real", "ai"]:

    folder = os.path.join("dataset", category)

    for filename in os.listdir(folder):

        path = os.path.join(folder, filename)

        if not os.path.isfile(path):
            continue

        try:
            with open(path, "rb") as image:

                response = requests.post(
                    API_URL,
                    files={"file": image}
                )

            data = response.json()

            print(data)

            score = data.get("consistency_score")

            # Handle insufficient geometry
            if score is None:

                score = "insufficient_geometry"
                prediction = "unknown"

            else:

                if score >= 0.25:
                    prediction = "real"
                else:
                    prediction = "ai"

            results.append([
                filename,
                category,
                score,
                prediction
            ])

            print(f"{filename} -> {score} -> {prediction}")

        except Exception as e:

            print(f"Error processing {filename}: {e}")

            results.append([
                filename,
                category,
                "error",
                "error"
            ])

with open(
    "results.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "filename",
        "type",
        "score",
        "prediction"
    ])

    writer.writerows(results)

print("\nDone!")
print(f"Processed {len(results)} images.")