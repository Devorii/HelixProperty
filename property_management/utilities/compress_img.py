from fastapi import UploadFile
from PIL import Image
import io


def compress_image_in_memory(image_file: UploadFile, target_size_mb: int = 5) -> bytes:
    """
    Compress image received in-memory to the target size in MB.
    :param image_file: Image file uploaded by client
    :param target_size_mb: Target size in MB (default: 5MB)
    :return: Compressed image as bytes
    """
    # Convert MB to bytes
    target_size_bytes = target_size_mb * 1024 * 1024

    # Open image from the UploadFile (in-memory)
    with Image.open(image_file.file) as img:
        # Initial quality
        quality = 95
        
        # Save the image to a memory buffer in JPEG format
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        
        # Reduce quality to fit the target size
        while buffer.tell() > target_size_bytes and quality > 10:
            buffer.seek(0)
            quality -= 5  # Reduce quality in steps of 5
            img.save(buffer, format="JPEG", quality=quality)
        
        # Return the compressed image in memory
        return buffer.getvalue()