"""
This script extracts and displays the most frequent keywords from a given text file.
It prompts the user for a file path, reads the text, removes common English stopwords,
and then counts the occurrences of each word to identify and print the top N keywords.
"""
import re
import nltk
from collections import Counter

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords

def extract_top_keywords(file_path, top_n=10):
    """
    Extracts the top N most common keywords from a text file, excluding English stopwords.
    Args:
        file_path (str): Path to the text file to analyze.
        top_n (int, optional): Number of top keywords to return. Defaults to 10.
    Returns:
        list of tuple: A list of (keyword, count) tuples representing the most common keywords.
    Raises:
        FileNotFoundError: If the specified file does not exist.
        Exception: For other I/O related errors.
    """
    stop_words = set(stopwords.words('english'))

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            text = file.read()

    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in stop_words]
    word_counts = Counter(filtered_words)
    most_common = word_counts.most_common(top_n)

    return most_common

if __name__ == "__main__":
    file_path = input("Enter the path to the text file: ")
    top_n = int(10)
    
    top_keywords = extract_top_keywords(file_path, top_n)
    print(f"Top {top_n} keywords:")
    for word, count in top_keywords:
        print(f"{word}: {count}")
