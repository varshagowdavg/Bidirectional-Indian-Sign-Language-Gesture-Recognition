from PIL import Image
import os

img_path = "backend/data/alphabets/chart.png"
if os.path.exists(img_path):
    img = Image.open(img_path)
    print(f"Image size: {img.size}")
else:
    print("Image not found")
