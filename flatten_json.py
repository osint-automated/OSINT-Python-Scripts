import json
import pandas as pd

json_file = input("Enter the name/PATH of the JSON file: ")

with open(json_file, 'r') as f:
    data = json.load(f)

def flatten_json(data):
    output = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for item in x:
                flatten(x[item], name + item + '_')

        elif isinstance (x, list):
            i = 0
            for item in x:
                flatten(item, name + str(i) + '_')
                i += 1

        else:
            output[name[:-1]] = x

    flatten(data)
    return output

if isinstance(data, list):
    flattened = [flatten_json(d) for d in data]
elif isinstance(data, dict):
    flattened = [flatten_json(d) for d in data["people"]] #replace people with JSON object name
else:
    flattened = [flatten_json(data)]

df = pd.DataFrame(flattened)

df.to_csv('flattened_json.csv', index=False)

pd.set_option('display.max_columns', None)
print(df.head())