import pandas as pd
from sqlalchemy import create_engine

# 1. CSV 파일 불러오기
df = pd.read_csv('goyong24_kdigital_courses.csv')

# 2. MySQL 연결 엔진 생성
engine = create_engine('mysql+pymysql://park:0120@127.0.0.1/work24db')

# 3. DataFrame을 'bootcampe' 테이블에 저장
df.to_sql(name='bootcampe', con=engine, if_exists='replace', index=False)

print("✅ CSV 데이터가 MySQL 'bootcampe' 테이블에 저장되었습니다.")
