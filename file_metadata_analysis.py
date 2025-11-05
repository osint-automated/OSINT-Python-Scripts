"""
This script extracts and displays metadata from a variety of file types.
It prompts the user for a file path and then uses libraries like mutagen, Pillow,
and PyPDF2 to extract and print metadata from media files, images, and PDFs.
"""
import os
import datetime
from mutagen import File
from PIL import Image
from PyPDF2 import PdfReader

def extract_metadata(file_path):
    """
    Extracts metadata from a given file, including general file properties and specific metadata for media, image, and PDF files.
    Parameters:
        file_path (str): The path to the file from which metadata will be extracted.
    Returns:
        dict: A dictionary containing metadata such as file name, size, creation/modification/access times, 
              and additional metadata for media (audio), image, and PDF files. Returns None if the file does not exist.
    Notes:
        - For media files, uses the `mutagen.File` class to extract metadata.
        - For image files, uses the `PIL.Image` class to extract metadata.
        - For PDF files, uses the `PyPDF2.PdfReader` class to extract metadata.
        - If the file is not of a supported type, only general file metadata is returned.
    """
    if not os.path.isfile(file_path):
        print("File does not exist.")
        return

    metadata = {
        'File Name': os.path.basename(file_path),
        'File Size (bytes)': os.path.getsize(file_path),
        'Created': datetime.datetime.fromtimestamp(os.path.getctime(file_path)),
        'Modified': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)),
        'Accessed': datetime.datetime.fromtimestamp(os.path.getatime(file_path)),
    }

    # Extract metadata for media files (audio)
    media_metadata = File(file_path)
    if media_metadata is not None:
        for key, value in media_metadata.items():
            metadata[key] = value

    # Extract metadata for image files
    try:
        with Image.open(file_path) as img:
            info = img.info
            if info:
                metadata['Image Metadata'] = info
                metadata['Creator'] = info.get('Author', 'N/A')
    except IOError:
        pass  # Not an image file

    # Extract metadata for PDF files
    try:
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            metadata['PDF Metadata'] = reader.metadata
            metadata['Creator'] = reader.metadata.get('/Creator', 'N/A')
    except Exception:
        pass  # Not a PDF file

    return metadata

def main():
    file_path = input("Enter the path to the file: ")
    metadata = extract_metadata(file_path)

    if metadata:
        for key, value in metadata.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
