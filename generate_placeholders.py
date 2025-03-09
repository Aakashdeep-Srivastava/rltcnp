"""
Generate placeholder images for the RTL Combinational Depth Predictor web application.
This script creates simple colored rectangles with text as placeholder images.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Create the images directory if it doesn't exist
os.makedirs('web/static/images', exist_ok=True)

def create_placeholder(filename, width, height, bg_color, text_color, text):
    """Create a placeholder image with text."""
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fall back to default if not available
    try:
        # Try to download a font from Google Fonts
        font_url = "https://github.com/google/fonts/raw/main/ofl/roboto/Roboto-Regular.ttf"
        response = requests.get(font_url)
        font = ImageFont.truetype(BytesIO(response.content), size=height//4)
    except Exception:
        # Fall back to default font
        try:
            font = ImageFont.truetype("arial.ttf", size=height//4)
        except Exception:
            font = ImageFont.load_default()
    
    # Calculate text position to center it
    text_width, text_height = draw.textsize(text, font=font)
    position = ((width - text_width) // 2, (height - text_height) // 2)
    
    # Draw the text
    draw.text(position, text, fill=text_color, font=font)
    
    # Save the image
    img.save(f'web/static/images/{filename}')
    print(f"Created {filename} ({width}x{height})")

def main():
    """Generate all placeholder images."""
    # Required images
    create_placeholder('logo.png', 200, 50, '#0d6efd', 'white', 'RTL Predictor')
    create_placeholder('favicon.png', 32, 32, '#0d6efd', 'white', 'RTL')
    create_placeholder('hero.jpg', 1200, 400, '#e9ecef', '#6c757d', 'RTL Circuit Design')
    
    # Feature icons
    create_placeholder('icon-upload.png', 24, 24, '#0d6efd', 'white', 'Up')
    create_placeholder('icon-predict.png', 24, 24, '#0d6efd', 'white', 'Pr')
    create_placeholder('icon-visualize.png', 24, 24, '#0d6efd', 'white', 'Vi')
    
    # Optional images
    create_placeholder('sample-counter.png', 400, 300, '#f8f9fa', '#333333', 'Counter RTL')
    create_placeholder('sample-alu.png', 400, 300, '#f8f9fa', '#333333', 'ALU RTL')
    create_placeholder('sample-fifo.png', 400, 300, '#f8f9fa', '#333333', 'FIFO RTL')
    
    create_placeholder('viz-feature-importance.png', 600, 400, '#f8f9fa', '#333333', 'Feature Importance')
    create_placeholder('viz-depth-prediction.png', 600, 400, '#f8f9fa', '#333333', 'Depth Prediction')
    
    create_placeholder('ui-upload.png', 800, 600, '#f8f9fa', '#333333', 'Upload UI')
    create_placeholder('ui-predict.png', 800, 600, '#f8f9fa', '#333333', 'Predict UI')
    create_placeholder('ui-results.png', 800, 600, '#f8f9fa', '#333333', 'Results UI')
    
    print("All placeholder images have been generated!")

if __name__ == "__main__":
    main() 