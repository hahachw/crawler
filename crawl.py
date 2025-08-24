from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time, re, json
from urllib.parse import urljoin, urlparse, parse_qs

# setting
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome()

def initcrawl():
    # crawling
    post_data = []
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

def crawl_everyIT():
    post_data = []
    url = "https://blog.naver.com/gridanews"
    driver.get(url)
    time.sleep(1)

    driver.switch_to.frame("mainFrame")
    #contw = driver.find_elements(By.CLASS_NAME, "contw-966")
    #headskin = contw.find_elements(By.ID, "head-skin")
    #bord = headskin.find_elements(By.ID, "whole-border")

    elements = driver.find_elements(By.CSS_SELECTOR, "ul.thumblist li.item a")

def get_categories():
    driver.get("https://blog.naver.com/gridanews")
    driver.switch_to.frame("mainFrame")

    cats = []
    anchors = driver.find_elements(By.CSS_SELECTOR, "#category-list a[href*='PostList.naver'][href*='categoryNo=']")
    seen = set()
    for a in anchors:
        href = (a.get_attribute("href") or "").strip()
        m = re.search(r"categoryNo=(\d+)", href)
        if not m: 
            continue
        cno = int(m.group(1))
        if cno in seen: 
            continue
        elif cno == 0:
            continue
        seen.add(cno)
        cats.append({
            "categoryNo": cno,
            "categoryName": a.text.strip(),
            "href": urljoin("https://blog.naver.com", href),
            "maxpage" : ""
        })

    driver.switch_to.default_content()
    
    # 파일 저장
    with open("everyones_IT/cate_info.json", "w", encoding="utf-8") as f:
        json.dump(cats, f, ensure_ascii=False, indent=2)
    print(len(cats))

def get_link_info():
    in_path = "everyones_IT/cate_info.json"
    out_path = "everyones_IT/link_info.json"
    base = "https://blog.naver.com"

    with open(in_path, "r", encoding="utf-8") as f:
        cats = json.load(f)

    results = []

    for c in cats:
        cno = c["categoryNo"]
        cname = c["categoryName"]
        href = c["href"].strip()  # 예: https://blog.naver.com/PostList.naver?blogId=gridanews&from=postList&categoryNo=25
        maxpage = int(c["maxpage"])

        for page in range(1, maxpage + 1):
            url = f"{href}&currentPage={page}"
            driver.get(url)
            time.sleep(0.8)

            # mainFrame 진입(있으면)
            try:
                driver.switch_to.frame("mainFrame")
            except Exception:
                pass

            # 글 링크 수집
            seen = set()
            for a in driver.find_elements(By.CSS_SELECTOR, "a[href*='PostView.naver'][href*='logNo=']"):
                h = (a.get_attribute("href") or "").strip()
                if not h:
                    continue
                if h.startswith("/"):
                    h = base + h
                # 페이지 내 중복 제거(간단히 logNo로)
                m = re.search(r"logNo=(\d+)", h)
                if not m:
                    continue
                ln = m.group(1)
                if ln in seen:
                    continue
                seen.add(ln)

                results.append({
                    "categoryNo": cno,
                    "categoryName": cname,
                    "page": page,
                    "postLink": h
                })

            # 프레임 복귀
            try:
                driver.switch_to.default_content()
            except Exception:
                pass

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def crawl_post_contents():
    in_path = "everyones_IT/link_info.json"
    out_path = "everyones_IT/post_data.json"

    with open(in_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    results = []
    cnt = 0
    for it in items:
        cnt += 1
        link = (it.get("postLink") or "").strip()
        if not link:
            continue
        
        driver.get(link)
        time.sleep(0.7)

        post_time = ""
        content = ""
        try:
            #print("1")
            #driver.switch_to.frame("mainFrame")
            print(cnt)

            # 게시 시점
            els = driver.find_elements(By.CSS_SELECTOR, "span.se_publishDate")
            if els:
                post_time = els[0].text.strip()

            # 본문
            if driver.find_elements(By.CLASS_NAME, "se-main-container"):
                container = driver.find_element(By.CLASS_NAME, "se-main-container")
                texts = container.find_elements(By.CLASS_NAME, "se-text")
                content = "\n\n".join(t.text.strip() for t in texts if t.text.strip())
            elif driver.find_elements(By.ID, "postViewArea"):
                container = driver.find_element(By.ID, "postViewArea")
                content = container.text.strip()
        except:
            post_time = post_time or ""
            content = content or ""
        finally:
            try:
                driver.switch_to.default_content()
            except:
                pass

        results.append({**it, "time": post_time, "content": content})

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[OK] {len(results)} posts -> {out_path}")

def crawl_mook():
    post_data = []
    categories = [
        {"category_id" : 6, "category_name" : "Mook's Life", "max_page" : 3},
        {"category_id" : 7, "category_name" : "Car", "max_page" : 215},
        {"category_id" : 19, "category_name" : "패션미용", "max_page" : 7},
        {"category_id" : 20, "category_name" : "푸드", "max_page" : 7},
        {"category_id" : 21, "category_name" : "리빙", "max_page" : 9},
        {"category_id" : 22, "category_name" : "생활건강", "max_page" : 12},
        {"category_id" : 23, "category_name" : "동물펫", "max_page" : 1},
        {"category_id" : 24, "category_name" : "운동", "max_page" : 1},
        {"category_id" : 17, "category_name" : "IT가전", "max_page" : 26},
        {"category_id" : 18, "category_name" : "남자아이템", "max_page" : 2},
        {"category_id" : 25, "category_name" : "육아", "max_page" : 3}
    ]

    for item in categories:
        id = item["category_id"]
        name = item["category_name"]
        pages = item["max_page"]
        for p in range(pages):
            url = f"https://blog.naver.com/PostList.naver?blogId=mookhuk1918&from=postList&categoryNo={id}&currentPage={p+1}"
            driver.get(url)
            time.sleep(1)

            #driver.switch_to.frame("mainFrame")
            elements = driver.find_elements(By.CSS_SELECTOR, "ul.thumblist li.item a")
            
            for el in elements:
                link = el.get_attribute("href")
                post_data.append({
                    "categoryNo" : id,
                    "category" : name,
                    "page" : p+1,
                    "link" : link
                })

            #driver.switch_to.default_content()
    
    out_path = "mook/link_info.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(post_data, f, ensure_ascii=False, indent=2)

def crawl_mook_additional():
    in_path = "mook/link_info_backup.json"
    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    post_data = []
    categories = [
        {"category_id" : 10, "category_name" : "맛집투어", "max_page" : 30},
        {"category_id" : 11, "category_name" : "Watch", "max_page" : 4},
        {"category_id" : 12, "category_name" : "분양정보", "max_page" : 30},
        {"category_id" : 16, "category_name" : "임용고시", "max_page" : 3},
    ]

    for item in categories:
        id = item["category_id"]
        name = item["category_name"]
        pages = item["max_page"]
        for p in range(pages):
            url = f"https://blog.naver.com/PostList.naver?blogId=mookhuk1918&from=postList&categoryNo={id}&currentPage={p+1}"
            post_data.append({
                "categoryNo" : id,
                "category" : name,
                "page" : p+1,
                "link" : url
            })
    
    data.extend(post_data)
    out_path = "mook/link_info.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def crawl_mook_reviews():
    in_path = "mook/link_info.json"
    out_path = "mook/link_info_test.json"

    # 1) 기존 데이터 로드 + 기존 logNo 집합
    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    lognos = set()
    for item in data:
        link = item.get("link", "")
        if not link:
            continue
        qs = parse_qs(urlparse(link).query)
        logno = qs.get("logNo", [None])[0]
        if logno:
            lognos.add(logno)

    # 2) Review(카테고리 8) 페이지 순회하며 추가 수집
    post_data = []
    for p in range(112):
        url = f"https://blog.naver.com/PostList.naver?from=postList&blogId=mookhuk1918&categoryNo=8&parentCategoryNo=8&currentPage={p+1}"
        driver.get(url)
        time.sleep(1)

        elements = driver.find_elements(By.CSS_SELECTOR, "ul.thumblist li.item a")
        for el in elements:
            href = (el.get_attribute("href") or "").strip()
            if not href:
                continue
            qs = parse_qs(urlparse(href).query)
            logno = qs.get("logNo", [None])[0]
            if not logno:
                continue
            if logno in lognos:
                continue  # 이미 있는 글이면 건너뜀

            lognos.add(logno)
            post_data.append({
                "categoryNo": 8,
                "category": "review",
                "page": p+1,
                "link": href
            })

    # 3) 기존 + 추가 저장
    data.extend(post_data)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[OK] added {len(post_data)} new posts, total -> {len(data)}")

def crawl_contents_mook():
    in_path = "mook/link_info.json"
    out_path = "mook/post_data.json"

    with open(in_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    results = []
    cnt = 0
    for it in items:
        cnt += 1
        link = (it.get("link") or "").strip()
        if not link:
            continue
        
        driver.get(link)
        time.sleep(0.7)

        post_time = ""
        content = ""
        try:
            #print("1")
            #driver.switch_to.frame("mainFrame")
            print(cnt)

            # 게시 시점
            els = driver.find_elements(By.CSS_SELECTOR, "span.se_publishDate")
            if els:
                post_time = els[0].text.strip()

            # 본문
            if driver.find_elements(By.CLASS_NAME, "se-main-container"):
                container = driver.find_element(By.CLASS_NAME, "se-main-container")
                texts = container.find_elements(By.CLASS_NAME, "se-text")
                content = "\n\n".join(t.text.strip() for t in texts if t.text.strip())
            elif driver.find_elements(By.ID, "postViewArea"):
                container = driver.find_element(By.ID, "postViewArea")
                content = container.text.strip()
        except:
            post_time = post_time or ""
            content = content or ""
        finally:
            try:
                driver.switch_to.default_content()
            except:
                pass

        results.append({**it, "time": post_time, "content": content})

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[OK] {len(results)} posts -> {out_path}")

crawl_mook_reviews()