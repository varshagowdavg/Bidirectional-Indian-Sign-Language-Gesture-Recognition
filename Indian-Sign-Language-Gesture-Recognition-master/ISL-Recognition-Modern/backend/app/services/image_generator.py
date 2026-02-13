"""
Image generation service for creating ISL gesture visualizations.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
import logging
from typing import List, Optional
import os

logger = logging.getLogger(__name__)


class ISLImageGenerator:
    """
    Generate ISL gesture images from text.
    Creates visual representations of sign language alphabets.
    """
    
    def __init__(self, alphabet_images_path: str = "data/alphabets"):
        """
        Initialize image generator.
        
        Args:
            alphabet_images_path: Path to directory containing ISL alphabet images
        """
        # Resolve path relative to backend root if needed
        base_path = Path(__file__).parent.parent.parent # backend/
        self.alphabet_path = base_path / alphabet_images_path
        
        if not self.alphabet_path.exists():
             # Try relative to current working directory
             self.alphabet_path = Path(alphabet_images_path)
             
        self.alphabet_cache = {}
        self._load_alphabet_images()
    
    def _load_alphabet_images(self):
        """Load ISL alphabet images into cache."""
        if not self.alphabet_path.exists():
            logger.warning(f"Alphabet images path does not exist: {self.alphabet_path}")
            logger.info("Will generate placeholder images")
            return
        
        # Load images for each letter
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            image_path = self.alphabet_path / f"{letter}.png"
            if image_path.exists():
                try:
                    img = Image.open(image_path)
                    self.alphabet_cache[letter] = img.copy()
                    logger.debug(f"Loaded image for letter: {letter}")
                except Exception as e:
                    logger.error(f"Error loading image for {letter}: {e}")
    
    def _create_placeholder_image(self, letter: str, size: tuple = (200, 200)) -> Image.Image:
        """
        Create a placeholder image for a letter.
        
        Args:
            letter: Letter to create placeholder for
            size: Image size (width, height)
            
        Returns:
            PIL Image
        """
        img = Image.new('RGB', size, color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fall back to default if not available
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 100)
            except:
                font = ImageFont.load_default()
        
        # Draw letter in center
        text = letter.upper()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        draw.text((x, y), text, fill=(50, 50, 50), font=font)
        
        # Add border
        draw.rectangle([(0, 0), (size[0]-1, size[1]-1)], outline=(100, 100, 100), width=2)
        
        return img
    
    def get_letter_image(self, letter: str) -> Image.Image:
        """
        Get image for a specific letter.
        
        Args:
            letter: Letter to get image for
            
        Returns:
            PIL Image
        """
        letter_lower = letter.lower()
        
        if letter_lower in self.alphabet_cache:
            return self.alphabet_cache[letter_lower].copy()
        else:
            # Create and cache placeholder
            placeholder = self._create_placeholder_image(letter_lower)
            self.alphabet_cache[letter_lower] = placeholder
            return placeholder.copy()
    
    def generate_word_image(
        self,
        word: str,
        output_path: Optional[str] = None
    ) -> Image.Image:
        """
        Generate image showing ISL gestures for a word.
        
        Args:
            word: Word to generate image for
            output_path: Optional path to save image
            
        Returns:
            PIL Image
        """
        # Filter to only alphabetic characters
        letters = [c for c in word.lower() if c.isalpha()]
        
        if not letters:
            # Return blank image if no valid letters
            return Image.new('RGB', (400, 200), color=(255, 255, 255))
        
        # Get images for each letter
        letter_images = [self.get_letter_image(letter) for letter in letters]
        
        # Calculate grid dimensions
        num_letters = len(letters)
        cols = min(4, num_letters)  # Max 4 columns
        rows = (num_letters + cols - 1) // cols
        
        # Image dimensions
        img_width = 200
        img_height = 200
        padding = 10
        
        # Create composite image
        total_width = cols * (img_width + padding) + padding
        total_height = rows * (img_height + padding) + padding + 50  # Extra for word label
        
        composite = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))
        
        # Add word label at top
        draw = ImageDraw.Draw(composite)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 30)
            except:
                font = ImageFont.load_default()
        
        text = f"ISL: {word.upper()}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (total_width - text_width) // 2
        draw.text((x, 10), text, fill=(0, 0, 0), font=font)
        
        # Place letter images in grid
        for idx, (letter, img) in enumerate(zip(letters, letter_images)):
            row = idx // cols
            col = idx % cols
            
            x = col * (img_width + padding) + padding
            y = row * (img_height + padding) + padding + 50
            
            # Resize image if needed
            img_resized = img.resize((img_width, img_height), Image.Resampling.LANCZOS)
            composite.paste(img_resized, (x, y))
        
        # Save if output path provided
        if output_path:
            composite.save(output_path)
            logger.info(f"Saved word image to {output_path}")
        
        return composite
    
    def generate_sentence_image(
        self,
        sentence: str,
        output_path: Optional[str] = None,
        max_words: int = 4
    ) -> Image.Image:
        """
        Generate image showing ISL gestures for a sentence.
        
        Args:
            sentence: Sentence to generate image for
            output_path: Optional path to save image
            max_words: Maximum number of words to display
            
        Returns:
            PIL Image
        """
        # Split into words
        words = sentence.split()[:max_words]
        
        if not words:
            return Image.new('RGB', (400, 200), color=(255, 255, 255))
        
        # Generate image for each word
        word_images = [self.generate_word_image(word) for word in words]
        
        # Stack images vertically
        total_width = max(img.width for img in word_images)
        total_height = sum(img.height for img in word_images) + 20 * len(word_images)
        
        composite = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))
        
        y_offset = 10
        for img in word_images:
            x = (total_width - img.width) // 2
            composite.paste(img, (x, y_offset))
            y_offset += img.height + 20
        
        # Save if output path provided
        if output_path:
            composite.save(output_path)
            logger.info(f"Saved sentence image to {output_path}")
        
        return composite


# Singleton instance
_image_generator = None


def get_image_generator() -> ISLImageGenerator:
    """Get singleton image generator instance."""
    global _image_generator
    
    if _image_generator is None:
        _image_generator = ISLImageGenerator()
    
    return _image_generator
