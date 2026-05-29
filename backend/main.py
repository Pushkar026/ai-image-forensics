from fastapi import FastAPI, UploadFile, File

from utils.image_processing import (
    decode_image,resize_image,
    convert_to_gray,
    detect_edges
)

from utils.perspective import detect_lines

app = FastAPI()


@app.get("/")
def home():

    return {
        "message": "Backend running"
    }


@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...)
):

    contents = await file.read()

    image = decode_image(contents)
    
    image = resize_image(
    image,
    max_width=1600
)

    gray = convert_to_gray(image)

    edges = detect_edges(gray)

    analysis = detect_lines(
        edges,
        image
    )

    return {
        "message": "Analysis complete",
        "lines_detected": analysis[
            "lines_detected"
        ],
        "vanishing_point": analysis[
            "vanishing_point"
        ],
        "consistency_score": analysis[
            "consistency_score"
        ]
    }