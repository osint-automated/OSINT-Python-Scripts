from PIL import Image

def convert_image(input_path, output_path, output_format):
    """
    Converts an image to a specified format and saves it to the given output path.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path where the converted image will be saved.
        output_format (str): Desired format for the output image (e.g., 'JPEG', 'PNG').

    Raises:
        Exception: If the image conversion fails for any reason.

    Example:
        convert_image('input.png', 'output.jpg', 'JPEG')
    """
    try:
        image = Image.open(input_path)
        image.save(output_path, format=output_format)
        print(f"Image converted successfully: {output_path}")
    except Exception as e:
        print(f"Error converting image: {e}")

if __name__ == "__main__":
    #ensure image is in same directory as script
    input_path = input('Enter image name here: ')
    output_path = f"{input_path}.png"
    output_format = input('Enter output format here: (ex. PNG, JPEG, etc.) ').upper()
    convert_image(input_path, output_path, output_format)