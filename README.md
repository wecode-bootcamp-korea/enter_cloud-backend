<img src="https://ibb.co/Ctjsdrq" />

# 🚀 프로젝트 소개 

    1차 프로젝트 [스페이스 클라우드] ("https://www.spacecloud.kr/")를 모티브로 프로젝트를 진행했습니다 

    2주라는 짧을 기간 제약이 있어 기획이 최소한으로 들어가는 사이트 클론 프로젝트를 선정했습니다 
    
    http method와 uri을 활용하여 restful 한 프로젝트를 지향합니다 

# 🚀 개발 방향 

개발기간 : 2021/1/11 ~ 2020/1/22 ( 2주간 진행 )

매일 데일리 미팅과 Sprint기간을 1주일로 잡고 매주 한번씩 Sprint 미팅을 통해 에자일하게 프로젝트를 진행했습니다 


# 🚀 팀원 

### Front_end 

- 김승완 <a href="https://github.com/wan-seung">Git hub</a>
- 문규찬 <a href="https://github.com/moonkyuchan">Git hub</a>

### Back_end

- 김준형 ( PM ) <a href="https://github.com/ddalkigum">Git hub</a>
- 윤정민 <a href="https://github.com/jeongmin14">Git hub</a>

# 🚀 적용 기술 및 구현 기능

### 공통

- AWS EC2, RDS 를 이용하여 배포를 진행했고, nohup으로 백그라운드로 돌아가도록 설정 
- Aquery Tool을 이용한 모델링 

### 백엔드 

- Python
- Django Framework
- Bcrypt를 이용한 단방향 해쉬 암호 저장, JWT Token을 이용한 유저 확인 
- RDBS인 Mysql을 사용 
- Django-seed를 활용한 커맨드를 만들어 가짜데이터로 통신을 주고 받음  

# 🚀 페이지별 구현 항목 

### /signin, /signup

- Bcrypt, JWT를 활용한 로그인, 회원가입 기능 구현 

### /spaces

- 메인페이지와 리스트 페이지 등... 여러 곳에서 필요한 공간 카드는 따로 View를 만들어 관리 

### /likes 

- 찜하기 기능, 찜한 공간 리스트 보여주기 


### 데모 영상(이미지 클릭)

유투브 : https://www.youtube.com/watch?v=s8qKmTRccPw

<br>


## Reference

- 이 프로젝트는 [스페이스 클라우드](https://www.spacecloud.kr/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.