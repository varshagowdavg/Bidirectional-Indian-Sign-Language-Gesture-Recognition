from PIL import Image
import os

def slice_image(image_path, output_dir):
    img = Image.open(image_path)
    width, height = img.size
    
    # Grid dimensions (guessed)
    rows = 4
    cols = 7
    
    cell_width = width // cols
    cell_height = height // rows
    
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    count = 0
    for row in range(rows):
        for col in range(cols):
            if count >= len(letters):
                break
            
            left = col * cell_width
            top = row * cell_height
            right = left + cell_width
            bottom = top + cell_height
            
            # Crop
            cell = img.crop((left, top, right, bottom))
            
            # Save
            letter = letters[count]
            cell.save(os.path.join(output_dir, f"{letter.lower()}.png"))
            print(f"Saved {letter.lower()}.png")
            
            count += 1

if __name__ == "__main__":
    slice_image("backend/data/alphabets/chart.png", "backend/data/alphabets")
