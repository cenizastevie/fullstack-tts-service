import numpy as np
from io import BytesIO
from PIL import Image

def preprocess_image(image_bytes):
    """
    Preprocess the image by converting it to grayscale and resizing it.

    Args:
        image_bytes (bytes): The original image in bytes.

    Returns:
        bytes: The preprocessed image in bytes.
    """
    # Load the image
    image = Image.open(BytesIO(image_bytes))
    
    # Convert to grayscale
    image = image.convert("L")
    
    # Resize the image to a standard size (e.g., 256x256)
    image = image.resize((256, 256))
    
    # Convert back to bytes
    output = BytesIO()
    image.save(output, format="JPEG")
    return output.getvalue()