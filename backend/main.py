from fastapi import FastAPI, UploadFile, File

from utils.image_processing import (
    decode_image,
    convert_to_gray,
    detect_edges
)

from utils.perspective import detect_lines

app = FastAPI()


@app.get("/")
def home():

    return {"message": "Backend running"}


@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):

    contents = await file.read()

    image = decode_image(contents)

    gray = convert_to_gray(image)

    edges = detect_edges(gray)

    line_count = detect_lines(edges, image)

    return {
        "message": "Analysis complete",
        "lines_detected": line_count
    }