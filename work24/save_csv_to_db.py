import pandas as pd
from sqlalchemy import create_engine

# 1. CSV 불러오기
df = pd.read_csv('work24_developer_jobs_with_roles.csv')

# 2. MySQL 연결 엔진 생성
engine = create_engine('mysql+pymysql://park:0120@127.0.0.1/work24db')

# 3. DataFrame → MySQL 저장 (테이블 이름: jobs)
df.to_sql(name='jobs', con=engine, if_exists='append', index=False)

print("✅ CSV 데이터가 DB에 저장되었습니다.")
