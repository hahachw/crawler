import json

def count_items(json_path: str) -> int:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return len(data)

# 사용 예시
path = "mook/link_info.json"
print(count_items(path))
