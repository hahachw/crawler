import json
import re
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from datetime import datetime

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

with open("datas/data.json", "r", encoding = "utf-8") as dt:
    data_list = json.load(dt)

with open("datas/score_data.json", "r", encoding = "utf-8") as sc:
    all_list = json.load(sc)

with open("datas/top5_data.json", "r", encoding = "utf-8") as tp:
    top5_list = json.load(tp)

def check_earliest_date():
    with open("datas/data.json", "r", encoding="utf-8") as f:
        data_list = json.load(f)

    dates = []
    for item in data_list:
        time_str = item.get("time", "")
        if "시간" in time_str:
            continue  # 상대시간은 건너뜀
        try:
            # '2025. 7. 14.' 형태 처리
            date = datetime.strptime(time_str.strip(), "%Y. %m. %d.")
            dates.append(date)
        except ValueError:
            continue  # 형식이 안 맞으면 무시

    earliest = min(dates)
    print(earliest.strftime("%Y. %m. %d."))

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
                "time" : post.get("time"),
                "category": post.get("category"),
                "keyword": post.get("keyword"),
                "tf_score": post.get("tf_score"),
                "rm_score": post.get("rm_score")
            })

    with open("datas/LLM_author_score_data.json", "w", encoding="utf-8") as f:
        json.dump(author_scores, f, ensure_ascii=False, indent=4)

def plot_author_scores(author_name):
    with open("datas/LLM_author_score_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    posts = data[author_name]
    xs, ys, nums, colors = [], [], [], []

    for post in posts:
        tf = post["tf_score"]
        rm = post["rm_score"]
        num = post["num"]
        xs.append(tf)
        ys.append(rm)
        nums.append(num)

        # 조건 만족 시 빨간색, 아니면 파란색
        if tf > 0.8 and rm > 2.3:
            colors.append("red")
        else:
            colors.append("blue")

    plt.figure(figsize=(12, 8))
    plt.scatter(xs, ys, c=colors, edgecolor='black')

    for x, y, num in zip(xs, ys, nums):
        plt.text(x - 0.03, y + 0.01, str(num), fontsize=9)

    plt.axvline(x=0.8, color='gray', linestyle='--', linewidth=1)
    plt.axhline(y=2.3, color='gray', linestyle='--', linewidth=1)

    plt.xlim(0, 1.0)
    plt.ylim(0, 3.1)

    plt.xlabel("TF Score")
    plt.ylabel("RM Score")
    plt.title(f"Author : {author_name}")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def make_data_for_tags():
    with open("datas/author_data_top5.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for post in data:
        post["tag"] = []

    with open("datas/data_top5_with_tag.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def plot_with_tags():
    # 태그 번호 → 이름 매핑 (네가 준 것 그대로 사용)
    tag_label_map = {
        "1": "1 : 홍보 목적",
        "2": "2 : 후기 / 리뷰",
        "3": "3 : 정보 제공",
        "4": "4 : 일상 공유",
        "5": "5 : 의견 주장"
    }

    # JSON 로드
    with open("datas/data_top5_with_tag.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 메인 태그별 카운트 (중복 제거)
    main_tag_count = defaultdict(int)

    for post in data:
        tags = post.get("tag", [])
        # 상위 태그만 추출해서 중복 제거
        main_tags = set(tag.split("-")[0] for tag in tags if tag and tag[0].isdigit())
        for main_tag in main_tags:
            main_tag_count[main_tag] += 1

    # tag_label_map의 모든 태그 키를 기준으로 정렬하여 0도 포함
    sorted_keys = sorted(tag_label_map.keys(), key=int)
    labels = [tag_label_map[k] for k in sorted_keys]
    counts = [main_tag_count.get(k, 0) for k in sorted_keys]

    # 시각화
    plt.figure(figsize=(9, 5))
    plt.bar(labels, counts, color='skyblue', edgecolor='black')
    plt.title("상위 태그별 포스트 수 (중복 제거, 0 포함)")
    plt.xlabel("상위 태그 의미")
    plt.ylabel("포스트 수")
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_with_tags_detail():
    # 태그 전체 구조 (상세 포함)
    tag_label_map_detail = {
        "1-a": "1-a : 제품 홍보",
        "1-b": "1-b : 장소 홍보",
        "1-c": "1-c : 콘텐츠 홍보",
        "1-d": "1-d : 앱/웹/서비스 홍보",
        "2":   "2 : 후기 / 리뷰",
        "3-a": "3-a : 사실 전달",
        "3-b": "3-b : 팁 / 가이드 제공",
        "4":   "4 : 일상 공유",
        "5":   "5 : 의견 주장"
    }

    # JSON 로드
    with open("datas/data_top5_with_tag.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    tag_count = defaultdict(int)

    for post in data:
        tags = set(post.get("tag", []))  # 세부 태그 중복 제거
        for tag in tags:
            tag_count[tag] += 1

    # tag_label_map_detail 순서대로 정렬, 없는 건 0 처리
    sorted_keys = list(tag_label_map_detail.keys())
    labels = [tag_label_map_detail[k] for k in sorted_keys]
    counts = [tag_count.get(k, 0) for k in sorted_keys]

    # 시각화
    plt.figure(figsize=(12, 6))
    plt.bar(labels, counts, color='orange', edgecolor='black')
    plt.title("세부 태그별 포스트 수")
    plt.xlabel("세부 태그 의미")
    plt.ylabel("포스트 수")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def format_everyones_IT():
    input_path = "datas/LLM_author_score_data.json"
    output_path = "datas/everyones_it_text.txt"

    # JSON 불러오기
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # '모두의IT' 데이터만 가져오기
    items = data.get("모두의IT", [])

    # rm_score → tf_score 순 정렬
    items_sorted = sorted(
        items,
        key=lambda x: (x.get("tf_score", 0), x.get("rm_score", 0)),
        reverse=True
    )

    # TXT 저장
    with open(output_path, "w", encoding="utf-8") as f:
        for item in items_sorted:
            num = item.get("num")
            tf_score = item.get("tf_score", 0)
            rm_score = item.get("rm_score", 0)
            raw_text = item.get("text", "")

            # 문장 단위 줄바꿈 (마침표, 느낌표, 물음표 기준)
            formatted_text = re.sub(r"(?<=[.!?])\s+", "\n", raw_text.strip())

            f.write(f"[num: {num}]\n")
            f.write(f"[tf_score: {tf_score:.6f}]\n")
            f.write(f"[rm_score: {rm_score:.6f}]\n")
            f.write(f"{formatted_text}\n\n")

def plot_tf_scores_IT():
    # 파일 경로
    path = "everyones_IT/text_fluoroscopy_data_IT.json"

    # 데이터 로드
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # tf_score 추출
    tf_scores = [d["tf_score"] for d in data if "tf_score" in d]

    # --- x축=tf_score, 점으로 분포(스트립 플롯) ---
    np.random.seed(0)
    y = np.random.normal(loc=0.0, scale=0.02, size=len(tf_scores))  # 겹침 방지용 세로 방향 아주 작은 지터

    #plt.figure(figsize=(10, 3))
    #plt.scatter(tf_scores, y, s=14, alpha=0.6, edgecolor="none")
    #plt.yticks([])  # y축 숨김 (분포만 보이도록)
    #plt.xlabel("tf_score")
    #plt.title("tf_score strip plot")
    #plt.grid(axis="x", linestyle="--", alpha=0.4)
    #plt.tight_layout()
    #plt.show()

    # (옵션) 히스토그램도 같이 보고 싶으면 아래 주석 해제
    plt.figure(figsize=(10, 3))
    plt.hist(tf_scores, bins=40, alpha=0.8)
    plt.xlabel("tf_score")
    plt.ylabel("count")
    plt.title("tf_score histogram")
    plt.tight_layout()
    plt.show()

def plot_tf_scores_with_date_IT():
    # 파일 경로
    path = "everyones_IT/text_fluoroscopy_data_IT.json"

    # 데이터 로드
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 날짜 변환 함수
    def parse_time(t):
        # "2025. 8. 10. 13:27" 또는 "2025. 08. 11." 형태 모두 처리
        t = t.strip().replace(".", "").replace("  ", " ")
        parts = t.split()
        if len(parts) == 3:  # 날짜만 있음
            return datetime.strptime(parts[0] + " " + parts[1] + " " + parts[2], "%Y %m %d")
        elif len(parts) == 4:  # 날짜 + 시간
            return datetime.strptime(parts[0] + " " + parts[1] + " " + parts[2] + " " + parts[3], "%Y %m %d %H:%M")
        else:
            raise ValueError(f"Unexpected time format: {t}")

    # 데이터에서 time과 tf_score 추출
    times, scores = [], []
    for d in data:
        if "tf_score" in d and "time" in d:
            try:
                times.append(parse_time(d["time"]))
                scores.append(d["tf_score"])
            except Exception as e:
                print("시간 파싱 실패:", d["time"], e)

    # 시각화
    plt.figure(figsize=(10, 6))
    plt.scatter(times, scores, alpha=0.6, edgecolor="k")
    plt.xlabel("Time")
    plt.ylabel("TF Score")
    plt.title("TF Score over Time")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_rm_scores_with_date_IT():
    # 파일 경로
    path = "everyones_IT/ReMoDetect_data_IT.json"

    # 데이터 로드
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 날짜 변환 함수
    def parse_time(t):
        # "2025. 8. 10. 13:27" 또는 "2025. 08. 11." 형태 모두 처리
        t = t.strip().replace(".", "").replace("  ", " ")
        parts = t.split()
        if len(parts) == 3:  # 날짜만 있음
            return datetime.strptime(parts[0] + " " + parts[1] + " " + parts[2], "%Y %m %d")
        elif len(parts) == 4:  # 날짜 + 시간
            return datetime.strptime(parts[0] + " " + parts[1] + " " + parts[2] + " " + parts[3], "%Y %m %d %H:%M")
        else:
            raise ValueError(f"Unexpected time format: {t}")

    # 데이터에서 time과 tf_score 추출
    times, scores = [], []
    for d in data:
        if "rm_score" in d and "time" in d:
            try:
                times.append(parse_time(d["time"]))
                scores.append(d["rm_score"])
            except Exception as e:
                print("시간 파싱 실패:", d["time"], e)

    # 시각화
    plt.figure(figsize=(10, 6))
    plt.scatter(times, scores, alpha=0.6, edgecolor="k")
    plt.xlabel("Time")
    plt.ylabel("RM Score")
    plt.title("RM Score over Time")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

#plot_with_tags_detail()
#plot_author_scores("모두의IT")
#format_everyones_IT()
plot_rm_scores_with_date_IT()