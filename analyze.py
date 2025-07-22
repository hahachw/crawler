import json
import matplotlib.pyplot as plt
import numpy as np

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

compare_bottom_posts()