"""
This script extracts and displays basic and EXIF metadata from an image file.
It prompts the user for the path to an image, then prints information such as
image format, size, and mode, as well as detailed EXIF data including camera
settings and GPS coordinates if available.
"""
from PIL import Image
import exifread

def get_basic_metadata(image_path):
    """Prints basic image information."""
    try:
        with Image.open(image_path) as img:
            print("\nBasic Image Information:")
            print(f"Format: {img.format}")
            print(f"Size: {img.size} pixels")
            print(f"Mode: {img.mode}")
    except Exception as e:
        print(f"Error opening image: {e}")


def convert_to_degrees(value):
    """
    Helper to convert EXIF GPS coordinates to decimal degrees.
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)
    return d + (m / 60.0) + (s / 3600.0)


def get_exif_data(image_path):
    """Extracts and prints EXIF metadata and GPS information."""
    try:
        with open(image_path, 'rb') as img_file:
            tags = exifread.process_file(img_file, details=False)

        print("\nEXIF Metadata:")
        exif_keys = [
            'Image Make', 'Image Model', 'Image DateTime',
            'EXIF FNumber', 'EXIF ExposureTime', 'EXIF ISOSpeedRatings',
            'EXIF FocalLength', 'EXIF LensModel'
        ]

        for tag in exif_keys:
            if tag in tags:
                print(f"{tag}: {tags[tag]}")

        # GPS Information
        gps_lat = tags.get('GPS GPSLatitude')
        gps_lat_ref = tags.get('GPS GPSLatitudeRef')
        gps_lon = tags.get('GPS GPSLongitude')
        gps_lon_ref = tags.get('GPS GPSLongitudeRef')

        if gps_lat and gps_lon and gps_lat_ref and gps_lon_ref:
            lat = convert_to_degrees(gps_lat)
            lon = convert_to_degrees(gps_lon)

            if str(gps_lat_ref) != 'N':
                lat = -lat
            if str(gps_lon_ref) != 'E':
                lon = -lon

            print("\nGPS Information:")
            print(f"Latitude: {lat:.6f}")
            print(f"Longitude: {lon:.6f}")
        else:
            print("\nNo GPS data found.")

    except Exception as e:
        print(f"Error reading EXIF data: {e}")


if __name__ == "__main__":
    image_path = input("Enter the path to the image file: ").strip().strip('"')
    get_basic_metadata(image_path)
    get_exif_data(image_path)
