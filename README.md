# dev-curation-airflow

Python Version: 3.12.11

## 개발 환경 설정

### 필수 요구사항
- Docker
- Docker Compose

### 개발 환경 시작하기

1. 개발 환경 실행
```shell
docker-compose -f docker-compose.dev.yml up -d
```

2. 데이터베이스 초기화
```shell
docker exec -it dev-curation-airflow-airflow-webserver-1 airflow db migrate
```

3. 관리자 계정 생성
```shell
docker exec -it dev-curation-airflow-airflow-webserver-1 airflow users create \
    --role Admin \
    --username admin \
    --email admin \
    --firstname admin \
    --lastname admin \
    --password admin
```

### 개발 환경 종료하기
```shell
docker-compose -f docker-compose.dev.yml down
```

### 접속 정보
- Airflow 웹 UI: http://localhost:8080
- 기본 관리자 계정
  - 아이디: admin
  - 비밀번호: admin
