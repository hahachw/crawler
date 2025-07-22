import json
import re

# 파일 경로 설정
input_path = "top5_data.json"       # 원본 JSON 파일
output_path = "formatted_text.txt"      # 결과 텍스트 파일

# JSON 불러오기
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 텍스트 파일로 저장
with open(output_path, "w", encoding="utf-8") as f:
    for item in data:
        num = item.get("num")
        raw_text = item.get("text", "")
        # 문장 단위로 줄바꿈 (마침표, 느낌표, 물음표 기준)
        formatted_text = re.sub(r"(?<=[.!?])\s+", "\n", raw_text.strip())
        # 출력 형식: [num] + 줄바꿈 텍스트
        f.write(f"[num: {num}]\n{formatted_text}\n\n")
