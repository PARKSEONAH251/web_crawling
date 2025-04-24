from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# 1. 셀레니움 옵션 설정
def run_crawling():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36")

    # 2. 드라이버 실행 (webdriver-manager로 자동 관리)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    total_pages = 8
    results = []

    try:
        for page in range(1, total_pages + 1):
            url = f"https://www.work24.go.kr/hr/a/a/1100/trnnCrsInf.do?dghtSe=A&traingMthCd=A&tracseTme=1&endDate=20260419&keyword1=&keyword2=&pageSize=10&orderBy=ASC&startDate_datepicker=2025-04-19&currentTab=1&topMenuYn=&pop=&tracseId=AIG20240000465106&pageRow=50&totamtSuptYn=A&keywordTrngNm=&crseTracseSeNum=&keywordType=1&gb=&keyword=%EA%B0%9C%EB%B0%9C%EC%9E%90&kDgtlYn=&ncs=2001%7C%EC%A0%84%EC%B2%B4&area=00%7C%EC%A0%84%EA%B5%AD+%EC%A0%84%EC%B2%B4&orderKey=2&mberSe=&kdgLinkYn=&srchType=all_type&totTraingTime=A&crseTracseSe=kdgtal_def_tgcr_yn%7CK-%EB%94%94%EC%A7%80%ED%84%B8%EA%B8%B0%EC%B4%88%EC%97%AD%EB%9F%89%ED%9B%88%EB%A0%A8%2Ckdgtal_tgcr_yn%7CK-%EB%94%94%EC%A7%80%ED%84%B8%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D%2Cmrfn_tlc_crse_yn_c0055%7C%EA%B5%AD%EB%AF%BC%EB%82%B4%EC%9D%BC%EB%B0%B0%EC%9B%80%EC%B9%B4%EB%93%9C%28%EC%9D%BC%EB%B0%98%C2%B7%EA%B5%AC%EC%A7%81%EC%9E%90%29&tranRegister=&mberId=&i2=A&pageId=2&programMenuIdentification=EBG020000000310&endDate_datepicker=2026-04-19&monthGubun=&pageOrder=2ASC&pageIndex={page}&bgrlInstYn=&startDate=20250419&crseTracseSeKDT=&gvrnInstt=&selectNCSKeyword=&action=trnnCrsInfPost.do"
            driver.get(url)
            try:
                # 모든 항목이 로드될 때까지 명시적 대기 (중요!)
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.list_status_info"))
                )
            except Exception as e:
                print(f"⚠️ 페이지 {page} 로딩 실패: {str(e)[:100]}...")
                continue

            time.sleep(random.uniform(2, 3))  # 서버 부하 방지용 랜덤 대기

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            rows = soup.select("div.list")  # 수정된 부분: div.box_table_wrap → div.list_status_info

            for row in rows:
                try:
                    def safe_select(selector, default=""):
                        el = row.select_one(selector)
                        return el.text.strip() if el else default

                    # 훈련기관명 (회사명)
                    institute = safe_select("div.company_title a")
                    # 주소요약
                    address_phone = safe_select("p.s1_r")
                    # 훈련과정명
                    course = safe_select("div.info_area a")
                
                    # 훈련기간
                    date =  ""
                    info_p = row.select_one("p.info")
                    if info_p:
                        spans = info_p.find_all("span")
                        if len(spans) > 1:
                            date = spans[1].get_text(strip=True)

                    results.append({
                        "훈련기관명": institute,
                        "주소/회사번호": address_phone,
                        "훈련과정명": course,
                        "훈련기간": date,
                    })
                except Exception as e:
                    print("⚠️ 데이터 파싱 에러:", e)
                    continue
    finally:
        driver.quit()

    # 5. DataFrame 생성 및 저장
    df = pd.DataFrame(results)
    df.drop_duplicates(inplace=True)
    df.to_csv(r"C:\Users\sum\Desktop\web_crawling_test\goyong24_kdigital_courses.csv", index=False, encoding='utf-8-sig')
    print("✅ 크롤링 완료 및 중복 제거: goyong24_kdigital_courses.csv 저장됨")
    print("크롤링 실행됨")