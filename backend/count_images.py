import os

folder = "dataset/ai"

image_extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)

count = len([
    f for f in os.listdir(folder)
    if f.lower().endswith(image_extensions)
])

print(f"Total images: {count}")