import json

with open("data.json", "r", encoding="utf-8") as f:
    data_list = json.load(f)

print(len(data_list))