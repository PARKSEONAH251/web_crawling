from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd

# 1. 셀레니움 옵션 설정
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 2. 드라이버 실행
driver = webdriver.Chrome(service=Service(), options=options)

# 3. 페이지 반복
total_pages = 56  # 전체 데이터가 556건일 경우 (10건/페이지 기준)
results = []

for page in range(1, total_pages + 1):
    url = f"https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do?basicSetupYn=&careerTo=&keywordJobCd=&occupation=131201%2C131202%2C133100%2C133101%2C133200%2C133300%2C133301%2C134100&seqNo=&cloDateEndtParam=&payGbn=&templateInfo=&rot2WorkYn=&shsyWorkSecd=&resultCnt=10&keywordJobCont=&cert=&moreButtonYn=&minPay=&codeDepth2Info=11000&currentPageNo={page}&eventNo=&mode=&major=&resrDutyExcYn=&eodwYn=&sortField=DATE&staArea=&sortOrderBy=DESC&keyword=%EA%B0%9C%EB%B0%9C%EC%9E%90&termSearchGbn=&carrEssYns=&benefitSrchAndOr=O&occupationParam=131201%2C131202%2C133100%2C133101%2C133200%2C133300%2C133301%2C134100&disableEmpHopeGbn=&actServExcYn=&keywordStaAreaNm=&maxPay=&emailApplyYn=&codeDepth1Info=11000&keywordEtcYn=&regDateStdtParam=&publDutyExcYn=&keywordJobCdSeqNo=&viewType=&exJobsCd=&templateDepthNmInfo=&region=&employGbn=&empTpGbcd=&computerPreferential=&infaYn=&cloDateStdtParam=&siteClcd=all&searchMode=Y&birthFromYY=&indArea=&careerTypes=&subEmpHopeYn=&tlmgYn=&academicGbn=&templateDepthNoInfo=&foriegn=&entryRoute=&mealOfferClcd=&basicSetupYnChk=&station=&holidayGbn=&srcKeyword=%EA%B0%9C%EB%B0%9C%EC%9E%90&academicGbnoEdu=noEdu&enterPriseGbn=&cloTermSearchGbn=&birthToYY=&keywordWantedTitle=&stationNm=&benefitGbn=&keywordFlag=&notSrcKeyword=&essCertChk=&depth2SelCode=&keywordBusiNm=&preferentialGbn=&rot3WorkYn=&regDateEndtParam=&pfMatterPreferential=&termContractMmcnt=&careerFrom=&laborHrShortYn=#scrollLoc"
    
    driver.get(url)
    time.sleep(3)  # 페이지 로딩 대기

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.select("tr[id^='list']")

    for row in rows:
        try:
            def safe_select(selector, default=""):
                el = row.select_one(selector)
                return el.text.strip() if el else default

            def safe_select_list(selector, index, default=""):
                els = row.select(selector)
                return els[index].text.strip() if len(els) > index else default

            company = safe_select("a.cp_name")
            title = safe_select("a.t3_sb")
            salary = safe_select("li.dollar span")
            career = safe_select_list("li.member span", 0)
            education = safe_select_list("li.member span", 1)
            work_type = safe_select("li.time span")
            location = safe_select("li.site p")
            deadline = safe_select("p.s1_r:nth-of-type(1)").replace("마감일 :", "").strip()
            reg_date = safe_select("p.s1_r:nth-of-type(2)").replace("등록일 :", "").strip()
            d_day = safe_select("strong.t3_sb")

            logo_el = row.select_one("span.logo_wrap img")
            logo = "https://www.work24.go.kr" + logo_el["src"] if logo_el else ""

            results.append({
                "회사명": company,
                "채용 제목": title,
                "급여": salary,
                "경력": career,
                "학력": education,
                "근무형태": work_type,
                "근무지역": location,
                "마감일": deadline,
                "등록일": reg_date,
                "D-day": d_day,
                "회사로고": logo
            })

        except Exception as e:
            print("⚠️ 에러 발생:", e)
            continue

# 4. 종료
driver.quit()

# 5. DataFrame 생성 및 중복 제거
df = pd.DataFrame(results)
df["급여"] = df["급여"].str.replace(r"[\n\t]+", " ", regex=True).str.strip()
df.drop_duplicates(inplace=True)  # ✅ 중복 제거

# 6. 저장
df.to_csv("work24_developer_jobs_deduped.csv", index=False, encoding='utf-8-sig')
print("✅ 크롤링 완료 및 중복 제거: work24_developer_jobs_deduped.csv 저장됨")
