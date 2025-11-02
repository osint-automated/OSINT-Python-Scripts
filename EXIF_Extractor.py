from PIL import Image
import exifread

def get_basic_metadata(image_path):
    with Image.open(image_path) as img:
        print('Basic Image Information:')
        print(f'Image Format: {img.format}')
        print(f'Image Size: {img.size} pixels')
        print(f'Image Mode: {img.mode}')

def get_exif_data(image_path):
    """
    Extracts and prints EXIF metadata and GPS information from an image file.
    Args:
        image_path (str): The path to the image file from which to extract EXIF data.
    Returns:
        None
    Prints:
        - Selected EXIF metadata fields such as camera make, model, date/time, aperture, exposure time, ISO, focal length, and lens model.
        - GPS latitude and longitude information if available.
    Requires:
        - The 'exifread' library for processing EXIF data.
    """
    with open(image_path, 'rb') as img_file:
        tags = exifread.process_file(img_file)

        print('Exif Metadata:')
        exif_keys = [
            'Image Make', 'Image Model', 'Image DateTime',
            'Exif FNumber','Exif ExposureTime','Exif ISOSpeedRatings',
            'ExifFocalLength','Exif LensModel'
        ]

        for tag in exif_keys:
            if tag in tags:
                print(f'{tag}: {tags[tag]}')

        print('GPS Information:')
        gps_latitude = tags.get('GPS GPSLatitude')
        gps_longitude = tags.get('GPS GPSLongitude')

        if gps_latitude and gps_longitude:
            print(f'Latitude: {gps_latitude}')
            print(f'Longitude: {gps_longitude}')

image_path = input('Enter the path to the image file: ')
get_basic_metadata(image_path)
get_exif_data(image_path)