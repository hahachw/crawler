import json
import re
import matplotlib.pyplot as plt
import numpy as np

def extract_year(time_str):
    # "2025. 8. 6. 7:00" → 2025 추출
    match = re.search(r"(\d{4})", time_str)
    return int(match.group(1)) if match else None

def plot_scores():
    with open("score_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    nums = [post["num"] for post in data]
    tf_scores = [post["tf_score"] for post in data]
    rm_scores = [post["rm_score"] for post in data]

    plt.figure(figsize=(14, 6))
    plt.plot(nums, tf_scores, label="TF Score (text_fluoroscopy)", alpha=0.7)
    plt.plot(nums, rm_scores, label="RM Score (ReMoDetect)", alpha=0.7)
    plt.xlabel("Sample Number (num)")
    plt.ylabel("Score")
    plt.title("TF Score vs RM Score by Sample Number")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_scores_IT():
    with open("everyones_IT/score_data_IT.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    nums = [post["num"] for post in data]
    tf_scores = [post["tf_score"] for post in data]
    rm_scores = [post["rm_score"] for post in data]

    plt.figure(figsize=(14, 6))
    plt.plot(nums, tf_scores, label="TF Score (text_fluoroscopy)", alpha=0.7)
    plt.plot(nums, rm_scores, label="RM Score (ReMoDetect)", alpha=0.7)
    plt.xlabel("Sample Number (num)")
    plt.ylabel("Score")
    plt.title("TF Score vs RM Score by Sample Number")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def scatter_plot():
    with open("score_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    tf_scores = [post["tf_score"] for post in data]
    rm_scores = [post["rm_score"] for post in data]

    plt.figure(figsize=(6, 6))
    plt.scatter(tf_scores, rm_scores, alpha=0.4, s=10)
    plt.xlabel("TF Score")
    plt.ylabel("RM Score")
    plt.title("TF vs RM Score Scatter")
    plt.grid(True)
    plt.show()

    corr = np.corrcoef(tf_scores, rm_scores)[0, 1]
    print(corr)

def scatter_plot_IT():
    with open("everyones_IT/score_data_IT.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    tf_scores = [post["tf_score"] for post in data]
    rm_scores = [post["rm_score"] for post in data]

    plt.figure(figsize=(6, 6))
    plt.scatter(tf_scores, rm_scores, alpha=0.4, s=10)
    plt.xlabel("TF Score")
    plt.ylabel("RM Score")
    plt.title("TF vs RM Score Scatter")
    plt.grid(True)
    plt.show()

    corr = np.corrcoef(tf_scores, rm_scores)[0, 1]
    print(corr)

def compare_top_posts():
    with open("text_fluoroscopy/5_percent_top.json", "r", encoding="utf-8") as tf:
        tf_data = json.load(tf)
    with open("ReMoDetect/5_percent_top.json", "r", encoding="utf-8") as rm:
        rm_data = json.load(rm)
    
    rm_dict = {post["num"]: post for post in rm_data}

    top5_posts = []
    for tf_post in tf_data:
        num = tf_post["num"]
        if num in rm_dict:
            rm_post = rm_dict[num]
            top5_posts.append({
                "num": num,
                "text": tf_post["text"],
                "category": tf_post["category"],
                "keyword": tf_post["keyword"],
                "tf_score": tf_post["score"],
                "rm_score": rm_post["score"]
            })

    with open("top5_data.json", "w", encoding="utf-8") as f:
        json.dump(top5_posts, f, ensure_ascii=False, indent=4)

    print(len(top5_posts))

def compare_bottom_posts():
    with open("text_fluoroscopy/5_percent_bottom.json", "r", encoding="utf-8") as tf:
        tf_data = json.load(tf)
    with open("ReMoDetect/5_percent_bottom.json", "r", encoding="utf-8") as rm:
        rm_data = json.load(rm)
    
    rm_dict = {post["num"]: post for post in rm_data}

    bottom5_posts = []
    for tf_post in tf_data:
        num = tf_post["num"]
        if num in rm_dict:
            rm_post = rm_dict[num]
            bottom5_posts.append({
                "num": num,
                "text": tf_post["text"],
                "category": tf_post["category"],
                "keyword": tf_post["keyword"],
                "tf_score": tf_post["score"],
                "rm_score": rm_post["score"]
            })

    with open("bottom5_data.json", "w", encoding="utf-8") as f:
        json.dump(bottom5_posts, f, ensure_ascii=False, indent=4)

    print(len(bottom5_posts))

def sort_by_scores_IT():
    file_path = "everyones_IT/score_data_IT.json"

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    rm_scores = [post["rm_score"] for post in data]
    min_rm = min(rm_scores)
    max_rm = max(rm_scores)
    print(f"{min_rm} {max_rm}")

    for item in data:
        rm = item["rm_score"]
        rm_norm = (rm - min_rm) / (max_rm - min_rm)
        item["rm_score_norm"] = rm_norm

    for item in data:
        item["total_score"] = item["tf_score"] + item["rm_score_norm"]

    # === 상위/하위 N개 출력 ===
    N = 10
    sorted_data = sorted(data, key=lambda x: x["total_score"], reverse=True)
    top_n = sorted_data[:N]
    bottom_n = sorted_data[-N:]
    
    top_path = "everyones_IT/score_data_top.json"
    bottom_path = "everyones_IT/score_data_bottom.json"

    with open(top_path, "w", encoding="utf-8") as f:
        json.dump(top_n, f, ensure_ascii=False, indent=4)

    with open(bottom_path, "w", encoding="utf-8") as f:
        json.dump(bottom_n, f, ensure_ascii=False, indent=4)

    filtered = [item for item in data if extract_year(item.get("time", "")) and extract_year(item["time"]) >= 2024]
    filtered_sorted = sorted(filtered, key=lambda x: x["total_score"])
    bottom_2023 = filtered_sorted[:N]

    filtered_path = "everyones_IT/score_data_bottom_2024.json"
    with open(filtered_path, "w", encoding="utf-8") as f:
        json.dump(bottom_2023, f, ensure_ascii=False, indent=4)

sort_by_scores_IT()