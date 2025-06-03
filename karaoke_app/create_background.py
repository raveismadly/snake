
from PIL import Image

# Create a white background image
img = Image.new('RGB', (1280, 720), color='white')
img.save('lyrics_background.png')

print("Background image created successfully")
