import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# 셀레니움 크롬 옵션 설정
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(), options=options)

# 링크 기본 템플릿
base_url = "https://linkareer.com/search?direction=DESC&p={page}&q=%EA%B0%9C%EB%B0%9C%EC%9E%90&sort=RELEVANCE&tab=open-activity"

results = []

# 🔁 1~8페이지 전체 순회
for page in range(1, 9):
    url = base_url.format(page=page)
    driver.get(url)
    time.sleep(random.uniform(3, 5))  # 차단 방지용 딜레이

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.select("div.ActivityListItem-ua__StyledWrapper-sc-46739bc-0")

    for item in items:
        try:
            # 썸네일 이미지
            img_el = item.select_one("img.img-thumbnail")
            img_url = img_el["src"] if img_el else ""

            # 기관명
            company = item.select_one("p.company-name").text.strip()

            # 제목
            title = item.select_one("p.title").text.strip()

            # 상세 링크
            href = item.select_one("a.link")["href"]
            full_url = "https://linkareer.com" + href

            # 마감일, 조회수
            info = item.select("div.jss1190 > p")
            deadline = info[0].text.strip() if len(info) > 0 else ""
            view_count = info[1].text.strip() if len(info) > 1 else ""

            results.append({
                "제목": title,
                "기관": company,
                "마감일": deadline,
                "조회수": view_count,
                "상세링크": full_url,
                "썸네일": img_url
            })

        except Exception as e:
            print("⚠️ 에러 발생:", e)
            continue

driver.quit()

# 데이터 저장
df = pd.DataFrame(results)
df.drop_duplicates(inplace=True)
df.to_csv("linkareer_개발자_진행중공고.csv", index=False, encoding='utf-8-sig')
print("✅ 크롤링 완료: linkareer_개발자_진행중공고.csv 저장됨")
