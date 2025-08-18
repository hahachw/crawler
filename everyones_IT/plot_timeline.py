import json, re, os
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates

# JSON 로드
with open("everyones_IT/post_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# "~시간 전" → "25.08.11"
for item in data:
    t = (item.get("time") or "").strip()
    if re.fullmatch(r"\d+\s*시간\s*전", t):
        item["time"] = "2025. 08. 11."

# 날짜별 집계
date_counts = Counter()
pat = re.compile(r"^\s*(\d{2,4})\.\s*(\d{1,2})\.\s*(\d{1,2})")
for item in data:
    t = (item.get("time") or "").strip()
    m = pat.match(t)
    if m:
        y, mth, d = map(int, m.groups())
        if y < 100:  # YY → 20YY 변환
            y += 2000
        date_counts[datetime(y, mth, d)] += 1

# DataFrame 정렬
df = pd.DataFrame(sorted(date_counts.items()), columns=["date", "count"])

# Plot
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df["date"], df["count"], marker="o")

# 날짜 포맷 & 간격
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

plt.xticks(rotation=0)
plt.xlabel("Date")
plt.ylabel("Number of Posts")
plt.title("Posts by Date")
plt.tight_layout()
plt.show()
