import hashlib
import io
from PIL import Image

def hash_pii(data_string):
    """Irreversibly hashes sensitive PII (like phone numbers) using SHA-256."""
    if not data_string:
        return data_string
    # Encodes the string to bytes, scrambles it, and returns a 64-character hex string
    return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

def sanitize_image_exif(image_file):
    """
    Opens an uploaded image, strips all EXIF metadata by re-saving it 
    into an in-memory bytes buffer, and returns the clean image file.
    """
    image = Image.open(image_file)
    image_format = image.format if image.format else 'JPEG'
    
    if image.mode in ('RGBA', 'P'):
        image = image.convert('RGB')
        
    buffer = io.BytesIO()
    image.save(buffer, format=image_format, quality=95)
    buffer.seek(0)
    
    return buffer