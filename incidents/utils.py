import io
import hashlib
import cloudinary.uploader
from PIL import Image

def sanitize_and_upload_image(file_obj, folder="evidence"):
    """
    Strips EXIF (GPS/location) metadata from an image and uploads it to Cloudinary.
    Returns the secure Cloudinary URL string.
    """
    # Open image using Pillow
    image = Image.open(file_obj)

    # Re-save image to memory without metadata
    image_data = list(image.getdata())
    clean_image = Image.new(image.mode, image.size)
    clean_image.putdata(image_data)

    buffer = io.BytesIO()
    image_format = image.format if image.format else 'JPEG'
    clean_image.save(buffer, format=image_format)
    buffer.seek(0)

    # Upload clean buffer to Cloudinary
    upload_result = cloudinary.uploader.upload(buffer, folder=folder)
    return upload_result.get("secure_url")


def hash_phone_number(phone_number: str) -> str:
    """Hashes citizen phone numbers using SHA-256 for complete privacy."""
    return hashlib.sha256(phone_number.encode('utf-8')).hexdigest()