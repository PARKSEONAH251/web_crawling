import pandas as pd
from sqlalchemy import create_engine

# 1. CSV 파일 불러오기
df = pd.read_csv('linkareer_개발자_진행중공고.csv')

# 2. MySQL 연결 엔진 생성 (사용자, 비밀번호, DB 이름 수정 필요)
engine = create_engine('mysql+pymysql://park:0120@127.0.0.1/work24db')

# 3. DataFrame을 '부트캠프' 테이블에 저장
df.to_sql(name='bootcampe', con=engine, if_exists='append', index=False)

print("✅ CSV 데이터가 MySQL '부트캠프' 테이블에 저장되었습니다.")
