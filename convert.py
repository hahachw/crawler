import json

def convert_for_text_fluoroscopy():
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

def convert_for_ReMoDetect():
    with open("data.json", "r", encoding="utf-8") as f:
        data_list = json.load(f)
    
    texts = [post["content"] for post in data_list]

    converted_list = {
        "original" : texts,
        "sampled" : texts.copy()
    }

    with open("naver_naver_blog.raw_data.json", "w", encoding="utf-8") as f:
        json.dump(converted_list, f, ensure_ascii=False, indent=4)

convert_for_text_fluoroscopy()
convert_for_ReMoDetect()