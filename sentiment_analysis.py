from transformers import pipeline
import textwrap

sentiment_pipeline = pipeline("sentiment-analysis")

file_path = input('Enter file name/path here: ')
data = ''

with open(file_path, 'r') as file:
        for line in file:
            data += line.strip()

chunks = textwrap.wrap(data, width=512, break_long_words=True)

results = []
for chunk in chunks:
  result = sentiment_pipeline(chunk)
  results.append(result[0])

total_score = 0
for result in results:
  total_score += result['score']

average_score = total_score / len(results)

average_score_to_percentage = average_score * 100

print('-' *40)
print(f"Sentiment Analysis Score for {file_path}: {average_score_to_percentage:.2f}% {result['label']}")
print('-' *40)