# 프로젝트 컨텍스트

## 목적
토스플레이스 스타일의 POS(Point of Sale) 데스크톱 앱 구현.
Qt6/QML 기반으로 토스 포스 앱의 UI/UX를 재현하고, 기본적인 POS 기능을 제공한다.

## 기술 스택
- **프레임워크**: Qt 6.5+
- **UI**: QML (Qt Quick Controls 2)
- **언어**: C++17
- **빌드**: CMake 3.25+
- **의존성 관리**: vcpkg (manifest mode)
- **데이터베이스**: SQLite (로컬 데이터)
- **로깅**: spdlog

## 프로젝트 규칙

### 코드 스타일
- **클래스명**: PascalCase (예: `ProductModel`, `OrderService`)
- **함수명**: camelCase (예: `addProduct`, `processPayment`)
- **멤버 변수**: m_ 접두사 (예: `m_products`, `m_totalAmount`)
- **파일명**: snake_case (예: `product_model.cpp`, `db_manager.h`)
- **들여쓰기**: 4칸 스페이스
- **중괄호**: K&R 스타일

### QML 스타일
- **컴포넌트명**: PascalCase (예: `ProductCard.qml`, `TossButton.qml`)
- **프로퍼티명**: camelCase (예: `productName`, `totalPrice`)
- **id**: camelCase (예: `productGrid`, `paymentPanel`)
- **required property**: 명시적 인터페이스 정의에 사용

### 아키텍처 패턴
- **Model-View**: QAbstractListModel + QML ListView/GridView
- **서비스 레이어**: 비즈니스 로직 분리 (OrderService, ReportService)
- **싱글톤**: DatabaseManager (앱 전역 데이터 액세스)
- **QML_ELEMENT**: C++ 타입을 QML에 노출

### 디렉토리 구조
```
toss-pos/
├── CMakeLists.txt          # 메인 빌드 설정
├── vcpkg.json              # 의존성 매니페스트
├── main.cpp                # 앱 진입점
├── qml/
│   ├── Main.qml            # 루트 윈도우
│   ├── pages/              # 페이지 컴포넌트
│   ├── components/         # 재사용 컴포넌트
│   └── theme/              # 디자인 시스템
├── src/
│   ├── models/             # 데이터 모델 (QAbstractListModel)
│   ├── services/           # 비즈니스 로직
│   └── database/           # 데이터 액세스
└── resources/              # 폰트, 아이콘
```

### 테스트 전략
- **단위 테스트**: Qt Test (C++ 모델, 서비스)
- **UI 테스트**: QML TestCase (컴포넌트 동작)
- **커버리지 목표**: 핵심 비즈니스 로직 80%

### Git 워크플로우
- **메인 브랜치**: main
- **기능 브랜치**: feature/기능명
- **버그 수정**: fix/이슈설명
- **커밋 메시지**: Conventional Commits (feat:, fix:, refactor:)

## 도메인 컨텍스트

### 핵심 용어
- **POS**: Point of Sale - 판매 시점 관리 시스템
- **상품(Product)**: 판매 항목 (예: 아메리카노, 라떼)
- **카테고리(Category)**: 상품 분류 (예: 커피, 음료, 디저트)
- **주문(Order)**: 고객이 구매하는 상품 묶음
- **주문 항목(OrderItem)**: 주문 내 개별 상품 (상품 + 수량)
- **결제(Payment)**: 주문에 대한 대금 수납

### 비즈니스 규칙
1. 주문은 최소 1개 이상의 주문 항목을 포함해야 한다
2. 결제 완료 후 주문은 수정 불가
3. 상품 가격은 0보다 커야 한다
4. 재고가 0인 상품은 주문 불가 (재고 관리 기능 구현 시)

### 사용자 페르소나
- **카페 사장님**: 매장 운영, 메뉴 관리, 매출 확인
- **직원**: 주문 접수, 결제 처리
- **고객**: (키오스크 모드) 셀프 주문

## 중요 제약사항

### 기술적 제약
- **오프라인 우선**: 인터넷 없이도 핵심 기능 동작 (SQLite 로컬 저장)
- **크로스 플랫폼**: Windows 10+, macOS 11+ 지원
- **성능**: 상품 목록 로딩 500ms 이내

### 디자인 제약
- **토스 디자인 시스템 준수**: 색상, 타이포그래피, 간격
- **직관적 UI**: 최소한의 학습 곡선
- **터치 친화적**: 향후 태블릿/키오스크 확장 고려

### 보안 제약
- 결제 정보는 로컬에 평문 저장 금지 (시뮬레이션 환경)
- 매출 데이터 백업 기능 제공 (향후)

## 외부 의존성

### Qt 모듈
- qt6-base: 핵심 기능
- qt6-declarative: QML 엔진
- qt6-quickcontrols2: UI 컴포넌트
- qt6-svg: SVG 아이콘 지원

### 외부 라이브러리
- sqlite3: 로컬 데이터베이스
- spdlog: 로깅 (디버깅, 오류 추적)

---

## 에이전트 팀 참고

이 프로젝트는 다음 에이전트들이 협업합니다:

| 별칭 | 역할 | 담당 |
|------|------|------|
| 달미 | 태스크 매니저 | 요구사항, 세션 관리 |
| 도산 | 아키텍트 | 설계, 분석 |
| 용산 | 코드 작성자 | 새 코드 구현 |
| 철산 | 코드 수정자 | 버그 수정, 리팩토링 |
| 영실 | 코드 리뷰어 | 품질 검사 |
| 사하 | 디자이너 | UI/UX 설계 |
| 지평 | 테스터 | 빌드, 테스트 |
| 인재 | DevOps | CI/CD |

자세한 내용은 `CLAUDE.md` 참조.
