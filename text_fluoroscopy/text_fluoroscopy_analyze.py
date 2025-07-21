import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

with open("text_fluoroscopy/text_fluoroscopy_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)

def get_5_percent():
    sorted_data = sorted(data, key=lambda x: x["score"])
    bottom_5_percent = sorted_data[:160]
    top_5_percent = sorted_data[-160:]

    with open("text_fluoroscopy/5_percent_bottom.json", "w", encoding="utf-8") as f:
        json.dump(bottom_5_percent, f, ensure_ascii=False, indent=4)

    with open("text_fluoroscopy/5_percent_top.json", "w", encoding="utf-8") as f:
        json.dump(top_5_percent, f, ensure_ascii=False, indent=4)

def plot_distribution():
    scores = [post["score"] for post in data]

    plt.figure(figsize=(10, 6))
    sns.histplot(scores, bins=50, color='skyblue', edgecolor='black')

    plt.title("Distribution of Text Fluoroscopy Scores", fontsize=16)
    plt.xlabel("Score", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_by_category():
    category_avg = df.groupby("category")["score"].mean().sort_values(ascending=False)
    category_var = df.groupby("category")["score"].var().reindex(category_avg.index)
    with open("text_fluoroscopy/category_variance.txt", "w", encoding="utf-8") as f:
        f.write(category_var.round(5).to_string())

    plt.figure(figsize=(10, 5))
    category_avg.plot(kind='bar', color='#66b3ff', edgecolor='black')
    plt.title("Average Score by Category", fontsize=16)
    plt.ylabel("Average Score")
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_by_keyword():
    keyword_avg = df.groupby("keyword")["score"].mean().sort_values(ascending=False)
    keyword_var = df.groupby("keyword")["score"].var().reindex(keyword_avg.index)
    with open("text_fluoroscopy/keyword_variance.txt", "w", encoding="utf-8") as f:
        f.write(keyword_var.round(5).to_string())

    plt.figure(figsize=(14, 6))
    keyword_avg.plot(kind='bar', color='#ffcc99', edgecolor='black')
    plt.title("Average Score by Keyword", fontsize=16)
    plt.ylabel("Average Score")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

get_5_percent()