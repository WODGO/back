# WodGo Backend API

WodGo는 운동 관리 애플리케이션의 백엔드 API입니다.

## 🚀 빠른 시작

### 필수 사항
- Python 3.9+
- Supabase 계정

### 설치 및 실행

1. **저장소 클론 및 이동**
```bash
cd /Users/gimjinhyeon/Desktop/project/wodgo/back
```

2. **가상 환경 활성화**
```bash
source venv/bin/activate
```

3. **패키지 설치**
```bash
pip install -r requirements.txt
```

4. **환경변수 설정**
`.env` 파일을 생성하고 다음 내용을 설정:
```env
# Application
APP_NAME=WodGo
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# Database - Supabase
SUPABASE_URL=https://vkhqpzbvbfofuwftqwky.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

5. **서버 실행**
```bash
uvicorn main:app --reload
```

서버가 http://127.0.0.1:8000 에서 실행됩니다.

## 📚 API 문서

### 인터랙티브 API 문서
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🔗 API 엔드포인트

### 인증 (Authentication)

#### 회원가입
```http
POST /api/auth/register
Content-Type: application/json

{
  "phone_number": "01012345678",
  "nickname": "사용자닉네임",
  "gender": "MALE",
  "age": 25,
  "weight": 70.5,
  "height": 175.5,
  "password": "password123",
  "level": "초급"
}
```

**응답 예시:**
```json
{
  "status": "success",
  "message": "회원가입이 완료되었습니다",
  "data": {
    "id": "e224c3b4-e000-455b-86eb-c7f216fa8ae5",
    "phone_number": "01012345678",
    "nickname": "사용자닉네임",
    "gender": "MALE",
    "age": 25,
    "weight": 70.5,
    "height": 175.5,
    "level": "초급",
    "created_at": "2025-07-01T10:22:20.209642+00:00"
  }
}
```

#### 로그인
```http
POST /api/auth/login
Content-Type: application/json

{
  "phone_number": "01012345678",
  "password": "password123"
}
```

**응답 예시:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 사용자 관리 (Users)

#### 내 프로필 조회
```http
GET /api/users/me
Authorization: Bearer {access_token}
```

#### 내 프로필 수정
```http
PUT /api/users/me
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nickname": "새로운닉네임",
  "age": 26,
  "weight": 72.0,
  "height": 176.0,
  "level": "중급"
}
```

### 시스템

#### 헬스체크
```http
GET /health
```

**응답:**
```json
{
  "status": "healthy",
  "environment": "development"
}
```

## 📝 회원가입 필드 상세

### 필수 필드

| 필드 | 타입 | 제약사항 | 설명 |
|------|------|----------|------|
| `phone_number` | string | 10-20자, 휴대폰 번호 형식 | 휴대폰 번호 |
| `nickname` | string | 2-10자, 한글/영문/숫자/언더스코어 | 사용자 닉네임 |
| `gender` | enum | MALE, FEMALE | 성별 |
| `age` | integer | 10-100 | 나이 |
| `weight` | decimal | 30.0-200.0 | 체중 (kg) |
| `height` | decimal | 100.0-250.0 | 키 (cm) |
| `password` | string | 6자 이상, 숫자 포함 | 비밀번호 |
| `level` | enum | 초급, 중급, 고급, 엘리트 | 운동 수준 |

### 유효성 검사

- **휴대폰 번호**: `01[0-9]-?[0-9]{4}-?[0-9]{4}` 형식
- **닉네임**: 한글, 영문, 숫자, 언더스코어만 허용
- **비밀번호**: 최소 6자, 숫자 1개 이상 포함

## 🛠 기술 스택

- **FastAPI**: 웹 프레임워크
- **Supabase**: 데이터베이스 (PostgreSQL)
- **SQLAlchemy**: ORM
- **Pydantic**: 데이터 검증
- **JWT**: 인증
- **bcrypt**: 비밀번호 해싱

## 📁 프로젝트 구조

```
back/
├── app/
│   ├── api.py                 # API 라우터 통합
│   ├── core/
│   │   ├── config.py         # 설정 관리
│   │   ├── database.py       # 데이터베이스 연결
│   │   └── supabase_client.py # Supabase 클라이언트
│   ├── models/
│   │   └── user.py           # SQLAlchemy 모델
│   ├── routers/
│   │   ├── auth_supabase.py  # 인증 라우터
│   │   └── users.py          # 사용자 관리 라우터
│   ├── schemas/
│   │   └── user.py           # Pydantic 스키마
│   └── services/
│       ├── auth.py           # 인증 서비스
│       ├── user.py           # 사용자 서비스
│       └── user_supabase.py  # Supabase 사용자 서비스
├── main.py                   # FastAPI 앱 진입점
├── requirements.txt          # 의존성 패키지
├── .env.example             # 환경변수 예시
└── README.md
```

## 🔐 보안 기능

- JWT 기반 인증
- 비밀번호 bcrypt 해싱
- CORS 설정
- 입력 데이터 유효성 검사
- SQL 인젝션 방지 (Pydantic + SQLAlchemy)

## 🧪 테스트

### curl을 사용한 API 테스트

**회원가입:**
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/register" \
-H "Content-Type: application/json" \
-d '{
  "phone_number": "01012345678",
  "nickname": "테스트유저",
  "gender": "MALE",
  "age": 25,
  "weight": 70.5,
  "height": 175.5,
  "password": "test123",
  "level": "초급"
}'
```

**로그인:**
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "phone_number": "01012345678",
  "password": "test123"
}'
```

## 📄 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 언제든지 연락해 주세요.