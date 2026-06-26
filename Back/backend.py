from fastapi import FastAPI
# BaseModel : 서버로 들어오는 데이터의 유형 미리 정의 (자료형, 이름 등)
# Field : 지정 시 구체적인 옵션
from pydantic import BaseModel, Field

app = FastAPI()

all_records = []
all_workout = {}

# 모델을 활용해서 데이터의 송수신을 규격화
# 서비스 에러가 줄어듬

class HealthRecord(BaseModel):
    user_id: str = Field(...)  # (...) : 필수데이터
    height : int
    weight : int
    workout : bool

# 베이스 모델 만들기
# 운동에 대한 정보 모델 만들기
class WorkoutInfo(BaseModel):

    wokind: str = Field(description='운동 종류를 의미함, 스쿼트, 헬스, 유산소 등..') # 운동종류(str)
    wocount: int  = Field(description='운동 횟수를 의미함. 얼마나 오랫동안 했는지') # 운동횟수(int)
    #ge : 이상, gt : 초과, le : 이하, lt : 미만
    wointensity: int = Field(ge=1, le=10, description='얼마나 강한 운동했는지, 1에서 10까지로 직접 표현')  # 운동강도(1~10까지의int)

# 함수 만들기
# -> get() 정보 출력
# -> post()

# 운동 기록이 저장되어야 함
@app.post('/workout/{user_id}')
async def record_daily(user_id:str, workout:WorkoutInfo):
    workout_data = workout.model_dump()

    # 1. '회원 아이디'가 있는지 확인
    # 회원 기록 저장, 기록이 아예 없다면 새로운 기록 추가
    # all_workout이라는 딕셔너리에 'user_id':[] 를 추가.
    if user_id not in all_workout:
        all_workout[user_id] = []

    # all_workout[user_id] -> 딕셔너리에 user_id라는 '키'가 가진 '값'
    # 값 : 비어있는 리스트.append(추가할 데이터 묶음)
    all_workout[user_id].append(workout)
    return {'message' : f'{user_id} 회원님의 운동 기록이 처리되었습니다.',
            'saved_data' : workout_data}

@app.get('/workout')
async def read_workout_record():
    return {'data' : all_workout}


@app.get("/workout/{user_id}")
async def print_my_workout(user_id:str):
    #1. 이 회원이 등록되어있는 회원인가?
    if user_id in all_workout:
    #2. 등록 회원이라면 기록을 반환
        return {'user_id':user_id, 'data':all_workout[user_id]}
    #3. 미등록 회원이라면 반환 불가 안내
    else:
        return { 'user_id' : user_id,
                 'message' : '이 회원은 운동 기록이 존재하지 않습니다.',
                 'data' : []
                }

# class PersonalInfo()
# api 설계 -> 어떤 주소 app.get(주소1), app.post(주소2) -> 주소 정의
# api 설계2 -> 어떤 데이터? app.get(주소1) : 개인정보

# get - 정보를 '읽어올때만'
@app.get('/record')
async def read_record():    
    return {'data' : all_records}

# post - 정보를 새로 입력할 때
@app.post('/record')
async def create_record(personal_info:HealthRecord):
    #기록이 들어오면 기록을 저장
    #.model_dump() -> 기록을 저장하기 위해 딕셔너리 형태로 추출해줌
    new_data = personal_info.model_dump()
    all_records.append(new_data)    
    return {'message' : f'''{personal_info.user_id}님의 데이터가 성공적으로 처리되었습니다.''',
        'total_record' : f'전체 회원 수 : {len(all_records)}'}
