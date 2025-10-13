import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def read_text_from_file(file_path):
    """
    Reads the entire content of a text file and returns it as a string.

    Args:
        file_path (str): The path to the text file to be read.

    Returns:
        str: The content of the file as a string.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If an I/O error occurs while reading the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

file_path = input("Enter the path to your text file: ")
text = read_text_from_file(file_path)

sentiment = sia.polarity_scores(text)

print('-' * 50)
print(f'Negative Rating: ', sentiment.get('neg'))
print(f'Neutral Rating: ', sentiment.get('neu'))
print(f'Positive Rating: ', sentiment.get('pos'))
print(f'Compound Rating: ', sentiment.get('compound'))
print('-' * 50)
