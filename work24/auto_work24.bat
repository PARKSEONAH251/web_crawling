@echo off
cd /d "C:\Users\parkseonah\web_crawling"

python work24.py
python save_csv_to_db.py

echo ✅ 크롤링 및 DB 저장 완료!
pause

