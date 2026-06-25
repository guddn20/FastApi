from fastapi import FastAPI
# BaseModel : 서버로 들어오는 데이터의 유형 미리 정의
from pydantic import BaseModel, Field

app = FastAPI()

# 모델을 활용해서 데이터의 송수신을 규격화
# 서비스 에러가 줄어듬

class HealthRecord(BaseModel):
    user_id : str = Field(...) #필수(...)
    height : int
    weight : int
    workout : bool

all_records = []
workout_records = []

#베이스 모델 만들기
#운동에 대한 정보 모델 만들기
class WorkoutInfo(BaseModel):
    #운동종류(str)
    type : str
    #운동횟수(int)
    count : int
    #운동강도(1~10까지의int)
    intense : int = Field(...,min_length=1, max_length=10)
    
#함수 만들기
#운동 기록이 저장되어야 함
@app.post('/workdout/{user_id}')
async def record_daily(workout:WorkoutInfo):
    
    health_info = workout.model_dump()
    workout_records.append(health_info)
    return 

    
    
# class PersonalInfo()
# api 설계 -> 어떤 주소 app.get(주소1), app.post(주소2) -> 주소 정의
# api 설계2 -> 어떤 데이터? app.get(주소1) : 개인정보

# get - 정보를 '읽어올때만'
@app.get('/record')
async def read_record():
    
    return('data', all_records)


# post - 정보를 새로 입력할 때
@app.post('/record')
async def create_record(personal_info:HealthRecord):
    #기록이 들어오면 기록을 저장
    #.model_dump() -> 기록을 저장하기 위해 딕셔너리 형태로 추출해줌
    new_data = personal_info.model_dump()
    all_records.append(new_data)
    
    return {'message' : f'데이터가 성공적으로 처리되었습니다!'}
