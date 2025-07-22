import json

def analyze_comma_ratio(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_chars = 0
    total_commas = 0
    results = []

    for item in data:
        text = item["text"]
        num_chars = len(text)
        num_commas = text.count(",")
        ratio = num_commas / num_chars if num_chars > 0 else 0

        results.append({
            "num": item["num"],
            "chars": num_chars,
            "commas": num_commas,
            "ratio": ratio
        })

        total_chars += num_chars
        total_commas += num_commas

    overall_ratio = total_commas / total_chars if total_chars > 0 else 0
    return results, overall_ratio

# 분석 실행
top5_results, top5_ratio = analyze_comma_ratio("top5_data.json")
bottom5_results, bottom5_ratio = analyze_comma_ratio("bottom5_data.json")

# 결과 출력
print("=== TOP 5 ===")
for r in top5_results:
    print(f"{r['num']}: chars={r['chars']}, commas={r['commas']}, ratio={r['ratio']:.4f}")
print(f"Average comma ratio (TOP 5): {top5_ratio:.4f}")

print("\n=== BOTTOM 5 ===")
for r in bottom5_results:
    print(f"{r['num']}: chars={r['chars']}, commas={r['commas']}, ratio={r['ratio']:.4f}")
print(f"Average comma ratio (BOTTOM 5): {bottom5_ratio:.4f}")
