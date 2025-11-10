from futurehouse_client import FutureHouseClient, JobNames
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('futurehouse_api_key')

query = input('Enter query here: ')

client = FutureHouseClient(
    api_key=api_key,
)

task_data = {
    "name": JobNames.OWL,
    "query": query,
}

task_response = client.run_tasks_until_done(task_data)

for response_item in task_response:
    print(response_item.answer)