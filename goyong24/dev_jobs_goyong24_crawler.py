import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# 1. 셀레니움 옵션 설정
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--log-level=3')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36")

# 2. 크롬 드라이버 수동 실행
chrome_driver_path = r"C:\Users\missp\chromedriver-win64\chromedriver.exe"  # 실제 경로로 수정
driver = webdriver.Chrome(
    service=Service(executable_path=chrome_driver_path),
    options=options
)

# 3. URL 템플릿 설정 (1~10 페이지 순회)
base_url = "https://work24.go.kr/hr/a/a/1100/trnnCrsInf.do?dghtSe=A&traingMthCd=A&tracseTme=124&endDate=20260505&keyword1=&keyword2=&pageSize=10&orderBy=ASC&startDate_datepicker=2025-05-05&currentTab=1&topMenuYn=&pop=&tracseId=ACG20243001028861&pageRow=10&totamtSuptYn=A&keywordTrngNm=&crseTracseSeNum=&keywordType=1&gb=&keyword=%EA%B0%9C%EB%B0%9C%EC%9E%90&kDgtlYn=&ncs=20%7C%EC%A0%84%EC%B2%B4&area=00%7C%EC%A0%84%EA%B5%AD+%EC%A0%84%EC%B2%B4&orderKey=2&mberSe=&kdgLinkYn=&srchType=all_type&totTraingTime=A&crseTracseSe=A%7C%EC%A0%84%EC%B2%B4&tranRegister=&mberId=&i2=A&pageId=2&programMenuIdentification=EBG020000000310&endDate_datepicker=2026-05-05&monthGubun=&pageOrder=2ASC&pageIndex={page}&bgrlInstYn=&startDate=20250505&crseTracseSeKDT=&gvrnInstt=&selectNCSKeyword=&action=trnnCrsInfPost.do"

results = []

# 4. 페이지 순회 (1~10 페이지)
for page in range(1, 11):
    url = base_url.format(page=page)
    driver.get(url)
    time.sleep(random.uniform(3, 5))  # 로딩 지연

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.select("div.list")  # 실제 구조에 따라 수정 필요

    for row in rows:
        try:
            def safe_select(selector, default=""):
                el = row.select_one(selector)
                return el.text.strip() if el else default

            institute = safe_select("div.company_title a")
            address_phone = safe_select("p.s1_r")
            course = safe_select("div.info_area a")

            date = ""
            info_p = row.select_one("p.info")
            if info_p:
                spans = info_p.find_all("span")
                if len(spans) > 1:
                    date = spans[1].get_text(strip=True)

            results.append({
                "훈련기관명": institute,
                "주소/회사번호": address_phone,
                "훈련과정명": course,
                "훈련기간": date
            })
        except Exception as e:
            print("⚠️ 데이터 파싱 에러:", e)
            continue

driver.quit()

# 5. CSV로 저장
df = pd.DataFrame(results)
df.drop_duplicates(inplace=True)
df.to_csv("goyong24_kdigital_courses.csv", index=False, encoding='utf-8-sig')
print("✅ 크롤링 완료: goyong24_kdigital_courses.csv 저장됨")
