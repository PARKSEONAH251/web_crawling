@echo off
cd /d "C:\Users\missp\Documents\GitHub\web_crawling\linkareer"

echo ▶ 크롤링 실행 중...
python linkareer.py

echo ▶ DB 저장 중...
python save_csv_to_db_bootcamp.py

echo ✅ 크롤링 및 DB 저장 완료!
pause
