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

def merge_for_text_fluoroscopy():
    with open("data.json", "r", encoding="utf-8") as f:
        data_list = json.load(f)
    texts = [post["content"] for post in data_list]
    categories = [post["category"] for post in data_list]
    keywords = [post["keyword"] for post in data_list]

    scores = []
    with open("text_fluoroscopy/final_epoch_testset0_probs.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "Score:" in line:
                score = float(line.strip().split("Score:")[1])
                scores.append(score)

    merged_list = []
    for i in range(3200):
        merged = {
            "num" : i+1,
            "text" : texts[i],
            "category" : categories[i],
            "keyword" : keywords[i],
            "score" : scores[i]
        }
        merged_list.append(merged)

    with open("text_fluoroscopy/text_fluoroscopy_data.json", "w", encoding="utf-8") as f:
        json.dump(merged_list, f, ensure_ascii=False, indent=4)

def merge_for_ReMoDetect():
    with open("data.json", "r", encoding="utf-8") as f:
        data_list = json.load(f)
    texts = [post["content"] for post in data_list]
    categories = [post["category"] for post in data_list]
    keywords = [post["keyword"] for post in data_list]

    scores = []
    with open("ReMoDetect/naver_naver.trained_trained_model_naver_gpt_scores.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "Score:" in line:
                score = float(line.strip().split("Score:")[1])
                scores.append(score)

    merged_list = []
    for i in range(3200):
        merged = {
            "num" : i+1,
            "text" : texts[i],
            "category" : categories[i],
            "keyword" : keywords[i],
            "score" : scores[i]
        }
        merged_list.append(merged)

    with open("ReMoDetect/ReMoDetect_data.json", "w", encoding="utf-8") as f:
        json.dump(merged_list, f, ensure_ascii=False, indent=4)

def merge_author_score_data():
    with open("datas/data.json", "r", encoding="utf-8") as f:
        data_list = json.load(f)
    
    with open("datas/score_data.json", "r", encoding="utf-8") as f:
        score_list = json.load(f)

    merged_list = []
    for i in range(len(score_list)):
        merged = score_list[i].copy()
        merged["author"] = data_list[i].get("author", "Unknown")
        merged_list.append(merged)

    with open("datas/score_data_with_author.json", "w", encoding="utf-8") as f:
        json.dump(merged_list, f, ensure_ascii=False, indent=4)

merge_author_score_data()