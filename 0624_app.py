# app.py 함수 작성하기.
# 1. 필요 모듈 임포트 단계
# FastAPI의 핵심 클래스인 FastAPI와 요청 객체 처리를 위한 Request를 임포트합니다.
# URL 경로에서 변수를 추출하고 제약조건을 걸기 위해 Path를 임포트합니다.
from fastapi import FastAPI, Path
# from fastapi import Request
import requests

url = "http://127.0.0.1:8000/"

# 2. FastAPI 애플리케이션 객체 생성
app = FastAPI()
# [GET] 기본 루트 경로 ('/') 요청 처리 - 서버가 잘 켜졌는지 확인하는 용도입니다.
@app.get('/') 
async def root(): 
	return {'message' : 'FastAPI 서버가 정상적으로 동작 중입니다!'} 


# 복습을 위해 새롭게 설계된 간단한 '강의 데이터베이스(DB)' 대용 딕셔너리입니다.
course_database = { 101: {'course_id': 101, 'title': '인공지능 입문', 'professor': '박 교수'}, 
	102: {'course_id': 102, 'title': '파이썬 웹 프로그래밍', 'professor': '김 교수'}, 
	103: {'course_id': 103, 'title': '자료구조와 알고리즘', 'professor': '이 교수'} } 

response = requests.get(url)

# 4. 경로 변수(Path Variable)를 활용하여 강의 ID를 매개변수로 받는 GET API 라우터를 완성하세요.
# [요구사항 1] 경로 규칙을 '/course/강의ID' 형태로 변경하세요.
# [요구사항 2] 강의 ID는 정수형 변수여야 합니다.
# [요구사항 3] Path() 함수를 사용하여 course_id가 반드시 '100보다 크거나 같은(ge=100)' 정수여야 한다는 제약조건을 추가하세요.
@app.get('/course/{course_id}') # TOdo: 변경된 경로 규칙을 문자열로 작성하세요 
async def get_course_info( course_id : int = Path(..., ge=100)): # TOdo: Path를 활용해 최소값 100 제약조건(ge)을 명시하세요. ): 

    # 5. 매개변수로 안전하게 전달받은 course_id를 사용하여 course_database에서 해당 강의 정보를 찾으세요.
    # 만약에 대비해 딕셔너리의 .get() 메서드를 활용하여 매칭되는 데이터가 없으면 안내 문구를 주도록 응답을 설계합니다.
    if get_course_info:
        print(f'조회 성공! 강의 ID {response.json().get('course_id')}는 {response.json().get('professor')}님의 {response.json().get('title')} 입니다.')
        return get_course_info
    else:
        return {"error": "해당 강좌 번호는 존재하지 않습니다."}


# if __name__ == "__main__":
#     # 강의ID 요청해보기
#     url = "http://127.0.0.1:8000/course/"
#     number = input("강의 ID : \n")
#     get_course_info(number)
