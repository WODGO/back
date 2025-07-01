# WodGo API 문서

## 📖 개요

WodGo Backend API는 운동 관리 애플리케이션을 위한 RESTful API입니다. 사용자 인증, 프로필 관리 등의 기능을 제공합니다.

**Base URL**: `http://127.0.0.1:8000`

## 🔐 인증

JWT(JSON Web Token) 기반 인증을 사용합니다.

### 인증 헤더 형식
```
Authorization: Bearer {access_token}
```

---

## 📋 API 엔드포인트

### 1. 회원가입

사용자 계정을 생성합니다.

**URL**: `/api/auth/register`  
**Method**: `POST`  
**인증**: 불필요

#### 요청 바디
```json
{
  "phone_number": "string",
  "nickname": "string",
  "gender": "MALE" | "FEMALE",
  "age": "integer",
  "weight": "number",
  "height": "number", 
  "password": "string",
  "level": "초급" | "중급" | "고급" | "엘리트"
}
```

#### 필드 제약사항
- `phone_number`: 10-20자, 휴대폰 번호 형식 (예: 01012345678)
- `nickname`: 2-10자, 한글/영문/숫자/언더스코어만 허용
- `gender`: MALE 또는 FEMALE
- `age`: 10-100 사이의 정수
- `weight`: 30.0-200.0 사이의 숫자 (kg)
- `height`: 100.0-250.0 사이의 숫자 (cm)
- `password`: 6자 이상, 숫자 1개 이상 포함
- `level`: 초급, 중급, 고급, 엘리트 중 하나

#### 응답 예시
**성공 (201):**
```json
{
  "status": "success",
  "message": "회원가입이 완료되었습니다",
  "data": {
    "id": "e224c3b4-e000-455b-86eb-c7f216fa8ae5",
    "phone_number": "01012345678",
    "nickname": "테스트유저",
    "gender": "MALE",
    "age": 25,
    "weight": 70.5,
    "height": 175.5,
    "level": "초급",
    "created_at": "2025-07-01T10:22:20.209642+00:00"
  }
}
```

**오류 (400):**
```json
{
  "detail": "이미 등록된 휴대폰 번호입니다"
}
```

---

### 2. 로그인

사용자 인증을 수행하고 토큰을 발급합니다.

**URL**: `/api/auth/login`  
**Method**: `POST`  
**인증**: 불필요

#### 요청 바디
```json
{
  "phone_number": "string",
  "password": "string"
}
```

#### 응답 예시
**성공 (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**오류 (401):**
```json
{
  "detail": "휴대폰 번호 또는 비밀번호가 올바르지 않습니다"
}
```

---

### 3. 내 프로필 조회

현재 로그인한 사용자의 프로필 정보를 조회합니다.

**URL**: `/api/users/me`  
**Method**: `GET`  
**인증**: 필요

#### 요청 헤더
```
Authorization: Bearer {access_token}
```

#### 응답 예시
**성공 (200):**
```json
{
  "id": "e224c3b4-e000-455b-86eb-c7f216fa8ae5",
  "phone_number": "01012345678",
  "nickname": "테스트유저",
  "gender": "MALE",
  "age": 25,
  "weight": 70.5,
  "height": 175.5,
  "level": "초급",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-07-01T10:22:20.209642+00:00",
  "updated_at": "2025-07-01T10:22:20.209642+00:00"
}
```

---

### 4. 내 프로필 수정

현재 로그인한 사용자의 프로필 정보를 수정합니다.

**URL**: `/api/users/me`  
**Method**: `PUT`  
**인증**: 필요

#### 요청 헤더
```
Authorization: Bearer {access_token}
```

#### 요청 바디 (모든 필드 선택사항)
```json
{
  "nickname": "string",
  "age": "integer",
  "weight": "number",
  "height": "number",
  "level": "초급" | "중급" | "고급" | "엘리트"
}
```

#### 응답 예시
**성공 (200):**
```json
{
  "id": "e224c3b4-e000-455b-86eb-c7f216fa8ae5",
  "phone_number": "01012345678",
  "nickname": "새로운닉네임",
  "gender": "MALE",
  "age": 26,
  "weight": 72.0,
  "height": 176.0,
  "level": "중급",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-07-01T10:22:20.209642+00:00",
  "updated_at": "2025-07-01T10:25:15.123456+00:00"
}
```

---

### 5. 특정 사용자 프로필 조회

특정 사용자의 프로필을 조회합니다. (관리자용)

**URL**: `/api/users/{user_id}`  
**Method**: `GET`  
**인증**: 필요

#### URL 파라미터
- `user_id`: 조회할 사용자의 UUID

#### 요청 헤더
```
Authorization: Bearer {access_token}
```

#### 응답 예시
**성공 (200):**
```json
{
  "id": "e224c3b4-e000-455b-86eb-c7f216fa8ae5",
  "phone_number": "01012345678",
  "nickname": "테스트유저",
  "gender": "MALE",
  "age": 25,
  "weight": 70.5,
  "height": 175.5,
  "level": "초급",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-07-01T10:22:20.209642+00:00",
  "updated_at": "2025-07-01T10:22:20.209642+00:00"
}
```

---

### 6. 헬스체크

서버 상태를 확인합니다.

**URL**: `/health`  
**Method**: `GET`  
**인증**: 불필요

#### 응답 예시
**성공 (200):**
```json
{
  "status": "healthy",
  "environment": "development"
}
```

---

### 7. 루트 엔드포인트

API 기본 정보를 조회합니다.

**URL**: `/`  
**Method**: `GET`  
**인증**: 불필요

#### 응답 예시
**성공 (200):**
```json
{
  "status": "success",
  "message": "Welcome to WodGo",
  "version": "1.0.0"
}
```

---

## 🚨 공통 오류 응답

### 인증 오류 (401)
```json
{
  "detail": "Could not validate credentials"
}
```

### 권한 없음 (403)
```json
{
  "detail": "비활성화된 계정입니다"
}
```

### 리소스 없음 (404)
```json
{
  "detail": "사용자를 찾을 수 없습니다"
}
```

### 유효성 검사 오류 (422)
```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "ensure this value is greater than or equal to 10",
      "type": "value_error.number.not_ge",
      "ctx": {"limit_value": 10}
    }
  ]
}
```

### 서버 오류 (500)
```json
{
  "detail": "회원가입 중 오류가 발생했습니다"
}
```

---

## 📡 HTTP 상태 코드

| 상태 코드 | 설명 |
|-----------|------|
| 200 | OK - 요청 성공 |
| 201 | Created - 리소스 생성 성공 |
| 400 | Bad Request - 잘못된 요청 |
| 401 | Unauthorized - 인증 실패 |
| 403 | Forbidden - 권한 없음 |
| 404 | Not Found - 리소스 없음 |
| 422 | Unprocessable Entity - 유효성 검사 실패 |
| 500 | Internal Server Error - 서버 오류 |

---

## 🔗 인터랙티브 문서

실행 중인 서버에서 다음 URL로 인터랙티브 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 🧪 테스트 예시

### curl을 사용한 API 테스트

#### 1. 회원가입
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

#### 2. 로그인
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "phone_number": "01012345678",
  "password": "test123"
}'
```

#### 3. 프로필 조회 (토큰 필요)
```bash
curl -X GET "http://127.0.0.1:8000/api/users/me" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 4. 프로필 수정 (토큰 필요)
```bash
curl -X PUT "http://127.0.0.1:8000/api/users/me" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-d '{
  "nickname": "새로운닉네임",
  "level": "중급"
}'
```

---

## 📝 추가 정보

- 모든 날짜/시간은 ISO 8601 형식으로 UTC 기준입니다.
- 토큰 만료 시간: Access Token(30분), Refresh Token(7일)
- 비밀번호는 bcrypt로 해싱되어 저장됩니다.
- 모든 API 응답은 JSON 형식입니다.