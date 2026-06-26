import requests

# 1. 회원정보등록
def register_personal_info(base_url):
    print("회원 정보 입력을 시작합니다.")
    user_id = str(input("아이디를 입력해주세요. : \n"))
    height = int(input("신장(cm) 정보를 입력해주세요. : \n"))
    weight = int(input("체중 정보(kg)를 입력해주세요. : \n"))
    
    workout_input = input("오늘 운동하셨나요? (y/n) : \n").lower().strip()

    is_workout = True if workout_input == 'y' else False
    
    #여기 키 값은 왜 이렇게 적었을까? -> BaseModel에서 만든 키와 일치시켜야한다.
    payload = {
               'user_id' : user_id,
               'height' : height,
               'weight' : weight,
               'workout' : is_workout
               }
    #request에 정해진 주소로 정보 전송
    response = requests.post(f'{base_url}/record', json=payload)
    if response.status_code == 200:
        print(f'{user_id} 회원님 반갑습니다! 정보가 성공적으로 등록되었습니다!')
    else :
        print(f'등록 실패! 카운터에 문의하세요. {response.status_code}')

# 2. 회원정보조회(관리자)
def print_personal_info(base_url):
    response = requests.get(f'{base_url}/record')
    if response.status_code == 200:
        print(f"회원 정보를 열람합니다. {response.json().get('data')}")

# 3. 운동정보등록 -> + 개인의 운동 정보가 계속 쌓이도록
def register_workout_record(base_url):
    print('회원님의 운동 정보 등록을 시작합니다.')
    # 어떤 유저가 기록했는지 알기 위해서 아이디를 물어봄
    #'유저' 기록 로그인이 된 상태에서 '세션' 저장
    user_id = str(input("아이디를 입력해주세요. : \n"))
    wokind = str(input("오늘 한 운동의 종류는 무엇입니까? : \n"))
    wocount = int(input("운동을 몇개나/얼마나 오래 하셨습니까? : \n"))
    wointensity = int(input("운동 강도를 1에서 10 사이의 숫자로 표현해주세요. : \n"))

    data = {
                    'wokind' : wokind,
                    'wocount' : wocount,
                    'wointensity' : wointensity
                    }   

    response = requests.post(f"{base_url}/workout/{user_id}", json=data)

    if response.status_code == 200:
        print(f"{user_id} 회원님의 운동 기록 정보가 성공적으로 등록되었습니다!")
    else:
        #422 에러 -> 입력 형식이 지정해놓은 타입과 맞지 않은 경우
        #404 에러 -> 경로 잘못된 경우
        print(f"등록 실패! 카운터에 문의하세요. {response.status_code}")

# 4. 운동정보조회(관리자)
def print_workout_record(base_url):
    response = requests.get(f"{base_url}/workout")
    if response.status_code == 200:
        print(f"모든 회원의 운동 정보를 열람합니다. {response.json().get('data')}")

# 5. 운동정보조회(회원)
def print_my_workout_record(base_url):
    user_id = input('조회할 회원 아이디를 입력하세요. \n')
    
    #주소로 request 요청을 보냄
    response = requests.get(f"{base_url}/workout/{user_id}")
    
    if response.status_code == 200:
        result = response.json() # 서버에서 반환받은 데이터(result)

        #기록이 없는 회원
        if 'message' in result:
            print(f'{result.get('message')}')
        else:
            print(f'{result.get('user_id')} 회원님의 운동 기록')
            #result.get('data', []) => 'data'가 있으면 그대로 출력
            #'data'라는 키가 없으면 빈 [] 출력
            print(f'{result.get('data', [])}')
    else:
        print("에러 발생 : ", response.status_code)

if __name__ == '__main__':
    server_url = 'http://127.0.0.1:8000'
    # 5. (1 ~ 4) 몇 번 메뉴를 수행할 것인가?

    while True:
        print("\n========================================") 
        print(" 건강 및 운동 데이터 통합 시스템 ") 
        print("========================================")
        print(" 1. 대시보드 - 신체 정보 등록 (POST)") 
        print(" 2. 대시보드 - 전체 신체 정보 조회 (GET)") 
        print(" 3. 기록실 - 오늘의 상세 운동 등록 (POST)") 
        print(" 4. 기록실 - 전체 운동 기록 조회 (GET)") 
        print(" 5. 기록실 - 개인 운동 기록 조회 (GET)")
        print(" 6. 시스템 종료 (EXIT)") 
        print("========================================") 

        number = input("수행할 작업 번호를 선택하세요 : 1-6").strip()

        # 함수, 변수 명명규칙 -> 팀별, 회사별..
        if number == '1' :
            register_personal_info(server_url)
        elif number == '2' :
            print_personal_info(server_url)
        elif number == '3' :
            register_workout_record(server_url)
        elif number == '4' :
            print_workout_record(server_url)
        elif number == "5":
            print_my_workout_record(server_url)
        elif number == '6' :
            print('시스템을 종료합니다. 좋은 하루 되세요 ^_^')
            break
        else:
            print(f'없는 메뉴입니다. 메뉴 번호를 다시 입력해주세요.')
