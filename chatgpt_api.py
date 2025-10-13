import openai
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

def OPENAI_GEN(data):
  """
  Generates a response from the OpenAI GPT-4o-mini model using the provided input data.

  Args:
    data (str): The input prompt or message to send to the language model.

  Prompts the user to enter their OpenAI API key, initializes the ChatOpenAI model,
  invokes the model with the given data, and prints the generated response.

  Returns:
    None
  """
  OPENAI_API_KEY = input('Enter API key here: ')
  llm = ChatOpenAI(model='gpt-4o-mini', api_key=OPENAI_API_KEY)
  prompt = llm.invoke(data)
  response = prompt.content
  print(response)

data = input('Enter prompt here: ')
results = OPENAI_GEN(data)
results





