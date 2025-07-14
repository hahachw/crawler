from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import json

categories = [
    {
        "category_id": 1,
        "category_name": "엔터테인먼트·예술",
        "keywords": [
            {"keyword_id": 5, "keyword_name": "문학·책"},
            {"keyword_id": 6, "keyword_name": "영화"},
            {"keyword_id": 7, "keyword_name": "공연·전시"},
            {"keyword_id": 8, "keyword_name": "미술·디자인"},
            {"keyword_id": 9, "keyword_name": "드라마"},
            {"keyword_id": 10, "keyword_name": "방송"},
            {"keyword_id": 11, "keyword_name": "음악"},
            {"keyword_id": 12, "keyword_name": "스타·연예인"},
            {"keyword_id": 13, "keyword_name": "만화·애니"}
        ]
    },
    {
        "category_id": 2,
        "category_name": "생활·노하우·쇼핑",
        "keywords": [
            {"keyword_id": 14, "keyword_name": "일상·생각"},
            {"keyword_id": 15, "keyword_name": "육아·결혼"},
            {"keyword_id": 16, "keyword_name": "반려동물"},
            {"keyword_id": 17, "keyword_name": "좋은글·이미지"},
            {"keyword_id": 18, "keyword_name": "패션·미용"},
            {"keyword_id": 19, "keyword_name": "인테리어·DIY"},
            {"keyword_id": 20, "keyword_name": "요리·레시피"},
            {"keyword_id": 21, "keyword_name": "상품리뷰"},
            {"keyword_id": 36, "keyword_name": "원예·재배"}
        ]
    },
    {
        "category_id": 3,
        "category_name": "취미·여가·여행",
        "keywords": [
            {"keyword_id": 22, "keyword_name": "게임"},
            {"keyword_id": 23, "keyword_name": "스포츠"},
            {"keyword_id": 24, "keyword_name": "사진"},
            {"keyword_id": 25, "keyword_name": "자동차"},
            {"keyword_id": 26, "keyword_name": "취미"},
            {"keyword_id": 27, "keyword_name": "국내여행"},
            {"keyword_id": 28, "keyword_name": "세계여행"},
            {"keyword_id": 29, "keyword_name": "맛집"}
        ]
    },
    {
        "category_id": 4,
        "category_name": "지식·동향",
        "keywords": [
            {"keyword_id": 30, "keyword_name": "IT·컴퓨터"},
            {"keyword_id": 31, "keyword_name": "사회·정치"},
            {"keyword_id": 32, "keyword_name": "건강·의학"},
            {"keyword_id": 33, "keyword_name": "비즈니스·경제"},
            {"keyword_id": 34, "keyword_name": "교육·학문"},
            {"keyword_id": 35, "keyword_name": "어학·외국어"}
        ]
    }
]

# setting
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome()

# crawling
post_data = []
for category in categories:
    for keyword in category["keywords"]:
        for page in range(1,11):
            # open url by category,keyword,page
            cate_num = category["category_id"]
            key_num = keyword["keyword_id"]
            url = "https://section.blog.naver.com/ThemePost.naver?directoryNo={}&activeDirectorySeq={}&currentPage={}".format(key_num,cate_num,page)
            driver.get(url)
            time.sleep(1)

            # get metadata of posts
            posts = driver.find_elements(By.CLASS_NAME, "list_post_article")
            for post in posts:
                # info
                info = post.find_element(By.CLASS_NAME, "info_author")
                author = info.find_element(By.CLASS_NAME, "name_author").text.strip()
                period = info.find_element(By.CLASS_NAME, "time").text.strip()

                # title
                desc = post.find_element(By.CLASS_NAME, "desc")
                title = desc.find_element(By.CLASS_NAME, "title_post").text.strip()
                link = desc.find_element(By.CLASS_NAME, "desc_inner").get_attribute("href")

                post_data.append({
                    "category" : category["category_name"],
                    "keyword" : keyword["keyword_name"],
                    "page" : page,
                    "author" : author,
                    "time" : period,
                    "title" : title,
                    "link" : link
                })

# get post contents
for post in post_data:
    driver.get(post["link"])
    time.sleep(1)

    print(post["link"])
    try:
        driver.switch_to.frame("mainFrame")
    except:
        print(f"iframe 진입 실패: {post['link']}")
        post["content"] = ""
        continue

    try:
        content = ""
        if driver.find_elements(By.CLASS_NAME, "se-main-container"):
            container = driver.find_element(By.CLASS_NAME, "se-main-container")
            texts = container.find_elements(By.CLASS_NAME, "se-text")
            content = "\n\n".join(t.text.strip() for t in texts if t.text.strip())
        elif driver.find_elements(By.ID, "postViewArea"):
            container = driver.find_element(By.ID, "postViewArea")
            content = container.text.strip()
        else:
            print(f"본문 구조 알 수 없음: {post['link']}")
        post["content"] = content
    except:
        print(f"본문 수집 실패: {post['link']}")
        post["content"] = ""

    driver.switch_to.default_content()

# save
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(post_data, f, ensure_ascii=False, indent=2)

driver.quit()