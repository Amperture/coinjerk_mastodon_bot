import json

def save_config(config):
    with open('config.json','w') as f:
        json.dump(config, f)

with open('config.json') as json_data_file:
    config = json.load(json_data_file)
