import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

with open("ReMoDetect/ReMoDetect_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)

def get_5_percent():
    sorted_data = sorted(data, key=lambda x: x["score"])
    bottom_5_percent = sorted_data[:160]
    top_5_percent = sorted_data[-160:]

    with open("ReMoDetect/5_percent_bottom.json", "w", encoding="utf-8") as f:
        json.dump(bottom_5_percent, f, ensure_ascii=False, indent=4)

    with open("ReMoDetect/5_percent_top.json", "w", encoding="utf-8") as f:
        json.dump(top_5_percent, f, ensure_ascii=False, indent=4)

def plot_distribution():
    scores = [post["score"] for post in data]

    plt.figure(figsize=(10, 6))
    sns.histplot(scores, bins=50, color='skyblue', edgecolor='black')

    plt.title("Distribution of ReMoDetect Scores", fontsize=16)
    plt.xlabel("Score", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_by_category():
    category_avg = df.groupby("category")["score"].mean().sort_values(ascending=False)
    category_var = df.groupby("category")["score"].var().reindex(category_avg.index)
    with open("ReMoDetect/category_variance.txt", "w", encoding="utf-8") as f:
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
    with open("ReMoDetect/keyword_variance.txt", "w", encoding="utf-8") as f:
        f.write(keyword_var.round(5).to_string())

    plt.figure(figsize=(14, 6))
    keyword_avg.plot(kind='bar', color='#ffcc99', edgecolor='black')
    plt.title("Average Score by Keyword", fontsize=16)
    plt.ylabel("Average Score")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def count_high_category():
    threshold = 2.3

    # 원래 df에서 등장한 category 순서 유지
    category_order = df['category'].drop_duplicates()

    # 전체 수 & high 수
    count_total = df.groupby('category').size()
    count_high = df[df['score'] > threshold].groupby('category').size()

    # 비율 계산
    high_ratio = (count_high / count_total).fillna(0)
    count_high = count_high.fillna(0).astype(int)
    count_total = count_total.astype(int)

    # 순서 재정렬 (df 등장 순서 기준)
    high_ratio = high_ratio.reindex(category_order)
    count_high = count_high.reindex(category_order).fillna(0).astype(int)
    count_total = count_total.reindex(category_order).fillna(0).astype(int)

    # 시각화
    plt.figure(figsize=(10, 5))
    ax = high_ratio.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title(f"Proportion of Score > {threshold} by Category")
    plt.ylabel("Ratio")
    plt.xlabel("Category")
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # 막대 위 텍스트 표시
    for i, (total, high, ratio) in enumerate(zip(count_total, count_high, high_ratio)):
        text = f"{high}/{total}\n{ratio:.2f}"
        ax.text(i, ratio * 0.4, text, ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.show()

def count_high_keyword():
    threshold = 2.3

    # 키워드 등장 순서 기준으로 고유값 리스트 추출
    keyword_order = df['keyword'].drop_duplicates()

    # 전체 수 & high score 수
    count_total = df.groupby('keyword').size()
    count_high = df[df['score'] > threshold].groupby('keyword').size()

    # 비율 계산
    high_ratio = (count_high / count_total).fillna(0)
    count_high = count_high.fillna(0).astype(int)
    count_total = count_total.astype(int)

    # 인덱스를 keyword 등장 순서로 재정렬
    high_ratio = high_ratio.reindex(keyword_order)
    count_high = count_high.reindex(keyword_order).fillna(0).astype(int)
    count_total = count_total.reindex(keyword_order).fillna(0).astype(int)

    # 시각화
    plt.figure(figsize=(14, 6))
    ax = high_ratio.plot(kind='bar', color='#ffcc99', edgecolor='black')
    plt.title(f"Proportion of Score > {threshold} by Keyword", fontsize=16)
    plt.ylabel("Ratio")
    plt.xlabel("Keyword")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # 텍스트 표시
    for i, (high, ratio) in enumerate(zip(count_high, high_ratio)):
        text = f"{high}"
        ax.text(i, ratio + 0.001, text, ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.show()

count_high_category()