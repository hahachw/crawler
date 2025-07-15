import json

with open("data.json", "r", encoding="utf-8") as f:
    data_list = json.load(f)

converted_list = []
for post in data_list:
    converted = {
        "text" : post["content"],
        "result" : 0
    }
    converted_list.append(converted)

with open("naver_blog.json", "w", encoding="utf-8") as f:
    json.dump(converted_list, f, ensure_ascii=False, indent=4)