import json
import re
import matplotlib.pyplot as plt
from collections import defaultdict

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

with open("datas/data.json", "r", encoding = "utf-8") as dt:
    data_list = json.load(dt)

with open("datas/score_data.json", "r", encoding = "utf-8") as sc:
    all_list = json.load(sc)

with open("datas/top5_data.json", "r", encoding = "utf-8") as tp:
    top5_list = json.load(tp)

def get_author_top5():
    author_list = []
    for post in top5_list:
        i = post["num"]-1
        post_author = {
            "num" : post["num"],
            "author" : data_list[i]["author"],
            "category": post["category"],
            "keyword": post["keyword"],
            "text": post["text"]
        }
        author_list.append(post_author)
    
    with open("datas/author_data_top5.json", "w", encoding="utf-8") as f:
        json.dump(author_list, f, ensure_ascii=False, indent=4)

def get_author_all():
    author_list = []
    for post in all_list:
        i = post["num"]-1
        post_author = {
            "num" : post["num"],
            "author" : data_list[i]["author"],
            "category": post["category"],
            "keyword": post["keyword"],
            "text": post["text"]
        }
        author_list.append(post_author)
    
    with open("datas/author_data_all.json", "w", encoding="utf-8") as f:
        json.dump(author_list, f, ensure_ascii=False, indent=4)

def make_txt_author_data():
    with open("datas/author_data_top5.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with open("datas/LLM_text_with_author.txt", "w", encoding="utf-8") as f:
        for item in data:
            num = item.get("num", "N/A")
            author = item.get("author", "N/A")
            category = item.get("category", "N/A")
            keyword = item.get("keyword", "N/A")
            raw_text = item.get("text", "")

            formatted_text = re.sub(r"(?<=[.!?])\s+", "\n", raw_text.strip())

            f.write(f"[num: {num}]\n")
            f.write(f"[author: {author}]\n")
            f.write(f"[category: {category}]\n")
            f.write(f"[keyword: {keyword}]\n")
            f.write(f"{formatted_text}\n\n")

def analyze_authors_top5():
    with open("datas/author_data_top5.json", "r", encoding="utf-8") as f:
        top5_auth_data = json.load(f)

    author_cnt = defaultdict(int)
    for post in top5_auth_data:
        author = post.get("author", "Unknown")
        author_cnt[author] += 1

    author_cnt_sorted_by_name = dict(sorted(author_cnt.items(), key=lambda x: x[0]))
    author_cnt_sorted_by_cnt = dict(sorted(author_cnt.items(), key=lambda x: x[1], reverse=True))
    author_cnt_sorted = [author_cnt_sorted_by_name, author_cnt_sorted_by_cnt]

    with open("datas/author_cnt_dict_top5.json", "w", encoding="utf-8") as f:
        json.dump(author_cnt_sorted, f, ensure_ascii=False, indent=4)


def analyze_authors_all():
    with open("datas/author_data_all.json", "r", encoding="utf-8") as f:
        top5_auth_data = json.load(f)

    author_cnt = defaultdict(int)
    for post in top5_auth_data:
        author = post.get("author", "Unknown")
        author_cnt[author] += 1

    author_cnt_sorted_by_name = dict(sorted(author_cnt.items(), key=lambda x: x[0]))
    author_cnt_sorted_by_cnt = dict(sorted(author_cnt.items(), key=lambda x: x[1], reverse=True))
    author_cnt_sorted = [author_cnt_sorted_by_name, author_cnt_sorted_by_cnt]

    with open("datas/author_cnt_dict_all.json", "w", encoding="utf-8") as f:
        json.dump(author_cnt_sorted, f, ensure_ascii=False, indent=4)

def plot_top5_author():
    with open("datas/author_cnt_dict_top5.json", "r", encoding="utf-8") as f:
        cnt_data = json.load(f)

    author_counts = cnt_data[0]

    authors = list(author_counts.keys())
    counts = list(author_counts.values())

    plt.figure(figsize=(12, 6))
    plt.bar(authors, counts, color='skyblue', edgecolor='black')
    plt.xticks(rotation=90)
    plt.xlabel("Author")
    plt.ylabel("Posts")
    plt.title("Number of posts per author (LLM score top 5%)")
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.show()

def get_scores_LLM_authors():
    with open("datas/author_cnt_dict_top5.json", "r", encoding="utf-8") as f:
        author_cnt_dicts = json.load(f)
        main_dict = author_cnt_dicts[1]
        target_authors = [author for author, cnt in main_dict.items() if cnt > 1]

    with open("datas/score_data_with_author.json", "r", encoding="utf-8") as f:
        merged_data = json.load(f)

    author_scores = defaultdict(list)
    for post in merged_data:
        author = post.get("author")
        if author in target_authors:
            author_scores[author].append({
                "num": post.get("num"),
                "text": post.get("text"),
                "category": post.get("category"),
                "keyword": post.get("keyword"),
                "tf_score": post.get("tf_score"),
                "rm_score": post.get("rm_score")
            })

    with open("datas/LLM_author_score_data.json", "w", encoding="utf-8") as f:
        json.dump(author_scores, f, ensure_ascii=False, indent=4)

#get_author_all()
#get_author_top5()
#make_txt_author_data()
#analyze_authors_all()
#plot_top5_author()
get_scores_LLM_authors()