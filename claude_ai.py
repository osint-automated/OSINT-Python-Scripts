import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

"""
This script interacts with the Anthropic Claude API to summarize user-provided text.
It prompts the user for an API key and the text to be summarized, then sends a request
to the Claude model to generate a concise summary in active voice. The summary is printed
to the console.
Steps:
1. Prompts for Anthropic API key.
2. Prompts for input text to summarize.
3. Sends a summarization request to Claude using the specified model and parameters.
4. Outputs the summarized text.
Requirements:
- The 'anthropic' Python package must be installed.
- A valid Anthropic API key is required.
"""

api_key = os.getenv('anthropic_api_key')

client = anthropic.Anthropic(
    api_key=api_key,
)

data = input('Enter the text: ')

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1000,
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Summarize the following into a concise paragraph using active voice: {data}"
                }
            ]
        }
    ]
)
print(message.content)