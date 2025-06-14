# dev-curation-airflow

![CI](https://github.com/skygl-dev/dev-curation-airflow/actions/workflows/ci.yml/badge.svg)


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

## 프로덕션 환경 설정

프로덕션 환경은 2대의 서버에 분산 구성됩니다:
- 서버 1: 데이터베이스(PostgreSQL), 메시지 브로커(Redis), Airflow Webserver, Airflow Scheduler
- 서버 2: Airflow Worker

### 사전 준비사항

1. Docker 네트워크 생성
```shell
sudo docker network create airflow_net
```

2. 환경 변수 파일 설정
- `.db.env`: 데이터베이스 서버 환경 변수
- `.prod.env`: Airflow 환경 변수
  - `AIRFLOW__CORE__FERNET_KEY` 생성:
    ```shell
    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    ```
  - `AIRFLOW__WEBSERVER__SECRET_KEY` 생성:
    ```shell
    python -c "import secrets; print(secrets.token_hex(16))"
    ```

### 서버 1 설정

1. 데이터베이스 서버 실행
```shell
sudo docker-compose -f docker-compose.db.yml up -d
```

2. Airflow 웹서버와 스케줄러 실행
```shell
sudo docker-compose -f docker-compose.airflow-main.yml up -d
```

3. 데이터베이스 초기화 (최초 1회)
```shell
sudo docker exec -it dev-curation-airflow_airflow-webserver_1 airflow db migrate
```

sudo docker exec -it dev-curation-airflow_airflow-webserver_1 	airflow celery inspect ping

4. 관리자 계정 생성 (최초 1회)
```shell
sudo docker exec -it dev-curation-airflow_airflow-webserver_1 airflow users create \
    --role Admin \
    --username admin \
    --email admin@example.com \
    --firstname admin \
    --lastname admin \
    --password your_secure_password
```

### 서버 2 설정

1. Airflow 워커 실행
```shell
sudo docker-compose -f docker-compose.airflow-worker.yml up -d
```

### 주의사항

1. 프로덕션 환경에서는 반드시 안전한 비밀번호를 사용하세요.
2. 환경 변수 파일(.env)은 버전 관리에서 제외하고 안전하게 관리하세요.
3. 서버 간 통신을 위해 필요한 포트(Redis: 6379, PostgreSQL: 5432)가 열려있어야 합니다.
4. 모든 서버가 동일한 시간대로 설정되어 있어야 합니다.
