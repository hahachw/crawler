import json

with open("text_fluoroscopy/text_fluroscopy_data.json", "r", encoding="utf-8") as tf:
    tf_data = json.load(tf)

with open("ReMoDetect/ReMoDetect_data.json", "r", encoding="utf-8") as rm:
    rm_data = json.load(rm)
