# BMS
### 사용법
(무조건 수정된 소스코만 commit할 것, db 및 다른거 복사된 파일 커밋 금지) 
1. VCS -> Commit
2. VCS -> Git -> Push(단축키 : Ctrl + Shift + K)
3. commit 메시지는 [본인이름 + add/edit 등등 적기]
### 주의사항

- 프로그램 실행할 때 관리자권한으로 실행할 것
- Commit 할때 BMS.imi, misc.imi 등 환경설정 파일 절대 금지
- copy.py는 BMS위치에서 실행할 것 (python COPY\copy.py)
- 수정된 소스코드 외에 commit 하지 말 것
- 폴더 이름에 Parse라고 붙어 있으면 소스코드
  그 외에는 복사된 파일
  

### 설치 라이브러리
(no module named 에러 해결 방법)
- File->Setting->Project:[Name] -> python Interpreter 에서 라이브러리 add(+버튼)

- beautifulsoup4
- pypiwin32
- pytz
- lxml
- olefile
- pycryptodomex
- 등등 더 있음

### 프로그램 실행순서

1. copy.py 실행
- python COPY\copy.py

2. Parse.py 실행
- python Parse.py

3. DB생성



