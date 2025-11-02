import re
import textwrap
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('openai_api_key')

client = OpenAI(api_key=openai_api_key)

'''
The script assumes there is a text file named 'sample_article.txt' in the same directory. If there isn't one, create a txt file with that name and add the article text to it for analysis.
'''

def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def preprocess_text(text: str):
    text = re.sub(r'\s+', ' ', text.strip())
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences

def chunk_text(text: str, max_chunk_size=3000):
    """
    Splits text into chunks of roughly max_chunk_size characters
    while preserving sentence boundaries.
    """
    sentences = preprocess_text(text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def analyze_disinformation_llm(article_text: str, model="gpt-4o-mini"):
    """
    Use an LLM to identify disinformation narratives in text.
    Handles long text by chunking internally.
    """
    chunks = chunk_text(article_text, max_chunk_size=3000)
    all_results = []

    for i, chunk in enumerate(chunks, start=1):
        print(f"Analyzing chunk {i}/{len(chunks)}...")
        prompt = f"""
        You are a disinformation analyst. 
        Read the following text and identify any disinformation/misinformation/influence operations narratives or manipulative claims. 
        For each, provide in plain text and active voice only (do not use Markdown, stars, or formatting):
        Disinformation Narrative Identified:

        Supporting Excerpts:

        Analysis of Disinformation or Misleading Framing:

        Text:
        {textwrap.shorten(chunk, width=4000, placeholder="...")}

        Write the answer using a technical, professional tone with active voice only and in plain text.
        """
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert in media analysis and disinformation detection."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        chunk_result = response.choices[0].message.content.replace("**", "")
        all_results.append(chunk_result)

    return "\n\n----------------------------\n\n".join(all_results)

if __name__ == "__main__":
    source = "sample_article.txt"
    article_text = load_text(source)

    sentences = preprocess_text(article_text)

    llm_results = analyze_disinformation_llm(article_text)

    with open("disinformation_analysis_output.txt", "w", encoding="utf-8") as f:
        f.write(llm_results)

    print("=== LLM-based Narrative Analysis ===")
    print(llm_results)
