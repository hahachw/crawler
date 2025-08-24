import json

def convert_for_text_fluoroscopy():
    with open("everyones_IT/post_data.json", "r", encoding="utf-8") as f:
        data_list = json.load(f)

    converted_list = []
    for post in data_list:
        converted = {
            "text" : post["content"],
            "result" : 0
        }
        converted_list.append(converted)

    with open("everyones_IT/naver_blog.json", "w", encoding="utf-8") as f:
        json.dump(converted_list, f, ensure_ascii=False, indent=4)

def convert_for_ReMoDetect():
    with open("everyones_IT/post_data.json", "r", encoding="utf-8") as f:
        data_list = json.load(f)
    
    texts = [post["content"] for post in data_list]

    converted_list = {
        "original" : texts,
        "sampled" : texts.copy()
    }

    with open("everyones_IT/naver_naver_blog.raw_data.json", "w", encoding="utf-8") as f:
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

def merge_for_text_fluoroscopy_IT():
    with open("everyones_IT/post_data_updated.json", "r", encoding="utf-8") as f:
        data_list = json.load(f)
    categoryNames = [post["categoryName"] for post in data_list]
    times = [post["time"] for post in data_list]
    contents = [post["content"] for post in data_list]

    scores = []
    with open("everyones_IT/final_epoch_testset0_probs_IT.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "Score:" in line:
                score = float(line.strip().split("Score:")[1])
                scores.append(score)

    merged_list = []
    for i in range(5493):
        merged = {
            "num" : i+1,
            "category" : categoryNames[i],
            "time" : times[i],
            "content" : contents[i],
            "tf_score" : scores[i]
        }
        merged_list.append(merged)

    with open("everyones_IT/text_fluoroscopy_data_IT.json", "w", encoding="utf-8") as f:
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

def merge_for_ReMoDetect_IT():
    with open("everyones_IT/post_data_updated.json", "r", encoding="utf-8") as f:
        data_list = json.load(f)
    categoryNames = [post["categoryName"] for post in data_list]
    times = [post["time"] for post in data_list]
    contents = [post["content"] for post in data_list]

    scores = []
    with open("everyones_IT/naver_naver.trained_trained_model_naver_gpt_scores_IT.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "Score:" in line:
                score = float(line.strip().split("Score:")[1])
                scores.append(score)

    merged_list = []
    for i in range(5493):
        merged = {
            "num" : i+1,
            "category" : categoryNames[i],
            "time" : times[i],
            "content" : contents[i],
            "rm_score" : scores[i]
        }
        merged_list.append(merged)

    with open("everyones_IT/ReMoDetect_data_IT.json", "w", encoding="utf-8") as f:
        json.dump(merged_list, f, ensure_ascii=False, indent=4)

def merge_tf_rm():
    with open("text_fluoroscopy/text_fluoroscopy_data.json", "r", encoding="utf-8") as tf:
        tf_data = json.load(tf)

    with open("ReMoDetect/ReMoDetect_data.json", "r", encoding="utf-8") as rm:
        rm_data = json.load(rm)

    merged_data = []
    for tf_post, rm_post in zip(tf_data, rm_data):
        merged_post = {
            "num": tf_post["num"],
            "text": tf_post["text"],
            "category": tf_post["category"],
            "keyword": tf_post["keyword"],
            "tf_score": tf_post["score"],
            "rm_score": rm_post["score"]
        }
        merged_data.append(merged_post)

    with open("score_data.json", "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

def merge_tf_rm_IT():
    with open("everyones_IT/text_fluoroscopy_data_IT.json", "r", encoding="utf-8") as tf:
        tf_data = json.load(tf)

    with open("everyones_IT/ReMoDetect_data_IT.json", "r", encoding="utf-8") as rm:
        rm_data = json.load(rm)

    merged_data = []
    for tf_post, rm_post in zip(tf_data, rm_data):
        merged_post = {
            "num": tf_post["num"],
            "text": tf_post["content"],
            "category": tf_post["category"],
            "time": tf_post["time"],
            "tf_score": tf_post["tf_score"],
            "rm_score": rm_post["rm_score"]
        }
        merged_data.append(merged_post)

    with open("everyones_IT/score_data_IT.json", "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

def merge_author_score_data():
    with open("datas/data.json", "r", encoding="utf-8") as f:
        data_list = json.load(f)
    
    with open("datas/score_data.json", "r", encoding="utf-8") as f:
        score_list = json.load(f)

    merged_list = []
    for i in range(len(score_list)):
        merged = score_list[i].copy()
        author_data = data_list[i]

        merged["author"] = author_data.get("author", "Unknown")

        raw_time = author_data.get("time", "")
        if "시간" in raw_time:
            merged["time"] = "2025. 7. 14."
        else:
            merged["time"] = raw_time.strip()

        merged_list.append(merged)

    with open("datas/score_data_with_author.json", "w", encoding="utf-8") as f:
        json.dump(merged_list, f, ensure_ascii=False, indent=4)

merge_tf_rm_IT()