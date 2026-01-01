# TossPlace POS 앱 기술 설계

## 1. 컨텍스트

### 1.1 배경
토스플레이스 스타일의 POS(Point of Sale) 데스크톱 앱을 Qt6/QML로 구현한다.
직관적이고 세련된 UI/UX로 카페 주문/결제 시스템을 구축하며,
토스의 깔끔한 디자인 철학을 반영한다.

### 1.2 제약사항
| 제약 | 설명 |
|------|------|
| 오프라인 우선 | 인터넷 없이 핵심 기능 동작 (SQLite 로컬 저장) |
| 크로스 플랫폼 | Windows 10+, macOS 11+ 지원 |
| 성능 | 상품 목록 로딩 500ms 이내 |
| 터치 친화적 | 향후 태블릿/키오스크 확장 고려 |

### 1.3 기술 스택
- **프레임워크**: Qt 6.5+
- **UI**: QML (Qt Quick Controls 2)
- **언어**: C++17
- **빌드**: CMake 3.25+
- **의존성 관리**: vcpkg (manifest mode)
- **데이터베이스**: SQLite
- **로깅**: spdlog

---

## 2. 목표 / 비목표

### 2.1 목표 (MVP)
- [x] 상품/카테고리 관리 (CRUD)
- [x] 터치 친화적 주문 인터페이스
- [x] 장바구니 관리 (추가/삭제/수량 변경)
- [x] 결제 처리 (현금/카드 시뮬레이션)
- [x] 일별/월별 매출 조회
- [x] 토스 디자인 시스템 적용

### 2.2 비목표 (Scope 외)
- [ ] 실제 카드 결제 연동 (PG사)
- [ ] 재고 관리 시스템
- [ ] 다중 사용자/권한 관리
- [ ] 프린터 연동 (영수증)
- [ ] 클라우드 동기화
- [ ] 멤버십/포인트 시스템

---

## 3. 아키텍처 결정

### 3.1 전체 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                        QML UI Layer                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │OrderPage│  │Payment  │  │Report   │  │Settings │        │
│  │         │  │Page     │  │Page     │  │Page     │        │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
│       │            │            │            │              │
│  ┌────┴────────────┴────────────┴────────────┴────┐        │
│  │              QML Components                     │        │
│  │  TossButton, ProductCard, OrderPanel, etc.     │        │
│  └────────────────────┬───────────────────────────┘        │
└───────────────────────┼─────────────────────────────────────┘
                        │ Q_PROPERTY / Q_INVOKABLE
┌───────────────────────┼─────────────────────────────────────┐
│                       │    C++ Backend Layer                │
│  ┌────────────────────┴───────────────────────┐             │
│  │              Models (QAbstractListModel)    │             │
│  │  ProductModel, CategoryModel, OrderModel   │             │
│  └────────────────────┬───────────────────────┘             │
│                       │                                      │
│  ┌────────────────────┴───────────────────────┐             │
│  │              Services (Business Logic)      │             │
│  │  OrderService, PaymentService, ReportService│            │
│  └────────────────────┬───────────────────────┘             │
│                       │                                      │
│  ┌────────────────────┴───────────────────────┐             │
│  │              DatabaseManager (Singleton)    │             │
│  │                    SQLite                   │             │
│  └─────────────────────────────────────────────┘             │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 패턴 선택

| 패턴 | 선택 | 이유 |
|------|------|------|
| Model-View | QAbstractListModel + QML | Qt 표준, 성능 최적화 |
| 서비스 레이어 | 별도 클래스 | 비즈니스 로직 분리, 테스트 용이 |
| 데이터 액세스 | 싱글톤 | 단일 DB 연결, 리소스 관리 |
| QML 노출 | QML_ELEMENT | Qt6 표준, 선언적 |
| 상태 관리 | Q_PROPERTY + Signal | Qt 네이티브 반응형 |

---

## 4. 디렉토리 구조

```
toss-pos/
├── CMakeLists.txt              # 메인 빌드 설정
├── vcpkg.json                  # 의존성 매니페스트
├── main.cpp                    # 앱 진입점
│
├── qml/
│   ├── Main.qml                # 루트 윈도우
│   ├── pages/
│   │   ├── OrderPage.qml       # 주문 화면 (메인)
│   │   ├── PaymentPage.qml     # 결제 화면
│   │   ├── ReportPage.qml      # 매출 조회 화면
│   │   └── SettingsPage.qml    # 설정 화면
│   ├── components/
│   │   ├── TossButton.qml      # 버튼
│   │   ├── TossCard.qml        # 카드 컨테이너
│   │   ├── ProductCard.qml     # 상품 카드
│   │   ├── CategoryBar.qml     # 카테고리 탭 바
│   │   ├── OrderPanel.qml      # 주문 목록 패널
│   │   └── OrderItemRow.qml    # 주문 항목 행
│   └── theme/
│       └── TossTheme.qml       # 테마 정의 (싱글톤)
│
├── src/
│   ├── models/
│   │   ├── product_model.h/.cpp
│   │   ├── category_model.h/.cpp
│   │   └── order_model.h/.cpp
│   ├── services/
│   │   ├── order_service.h/.cpp
│   │   └── report_service.h/.cpp
│   ├── database/
│   │   └── db_manager.h/.cpp
│   └── types/
│       ├── product.h
│       └── order.h
│
└── resources/
    ├── icons/
    └── sample_data.sql
```

---

## 5. 데이터베이스 스키마

### 5.1 테이블 정의

```sql
-- 카테고리
CREATE TABLE categories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    icon        TEXT,
    sort_order  INTEGER DEFAULT 0,
    created_at  TEXT DEFAULT (datetime('now', 'localtime'))
);

-- 상품
CREATE TABLE products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name        TEXT NOT NULL,
    price       INTEGER NOT NULL,
    image_url   TEXT,
    is_active   INTEGER DEFAULT 1,
    sort_order  INTEGER DEFAULT 0,
    created_at  TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- 주문
CREATE TABLE orders (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    order_no     TEXT NOT NULL UNIQUE,
    total        INTEGER NOT NULL,
    payment_type TEXT NOT NULL,
    status       TEXT DEFAULT 'COMPLETED',
    created_at   TEXT DEFAULT (datetime('now', 'localtime')),
    completed_at TEXT
);

-- 주문 항목
CREATE TABLE order_items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id    INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    quantity    INTEGER NOT NULL,
    unit_price  INTEGER NOT NULL,
    subtotal    INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### 5.2 샘플 데이터

```sql
-- 카테고리
INSERT INTO categories (name, icon, sort_order) VALUES
('커피', 'coffee', 1),
('음료', 'cup', 2),
('디저트', 'cake', 3),
('베이커리', 'bread', 4);

-- 상품
INSERT INTO products (category_id, name, price, sort_order) VALUES
(1, '아메리카노', 4500, 1),
(1, '카페라떼', 5000, 2),
(1, '바닐라라떼', 5500, 3),
(1, '카푸치노', 5000, 4),
(1, '에스프레소', 3500, 5),
(2, '자몽에이드', 5500, 1),
(2, '레몬에이드', 5000, 2),
(2, '아이스티', 4500, 3),
(3, '치즈케이크', 6500, 1),
(3, '티라미수', 7000, 2),
(3, '마카롱 세트', 8000, 3);
```

---

## 6. 핵심 클래스 설계

### 6.1 DatabaseManager (싱글톤)
- SQLite 연결 관리
- 테이블 생성/초기화
- 샘플 데이터 삽입
- CRUD 메서드

### 6.2 ProductModel (QAbstractListModel)
- 상품 목록 관리
- 카테고리 필터링
- QML ListView/GridView 바인딩

### 6.3 OrderModel (QAbstractListModel)
- 장바구니 (현재 주문) 관리
- 항목 추가/삭제/수량 변경
- 총액 계산

### 6.4 OrderService
- 주문 생성/저장
- 결제 처리 (시뮬레이션)
- 주문번호 생성

### 6.5 ReportService
- 일별/월별 매출 조회
- 주문 내역 조회

---

## 7. QML-C++ 통합

### 7.1 QML_ELEMENT 매크로
모든 C++ 클래스에 QML_ELEMENT 매크로 사용

### 7.2 CMake 설정
```cmake
qt_add_qml_module(toss-pos
    URI TossPos
    VERSION 1.0
    QML_FILES ...
    SOURCES ...
)
```

### 7.3 QML에서 사용
```qml
import TossPos

ProductModel {
    id: productModel
    categoryId: currentCategory
}
```

---

## 8. 위험 / 트레이드오프

### 8.1 SQLite
- **장점**: 설정 없음, 파일 기반, 크로스플랫폼
- **단점**: 동시 쓰기 제한
- **결정**: MVP에서 사용, 향후 확장 고려

### 8.2 싱글톤 DatabaseManager
- **장점**: 단일 연결 관리, 간단한 구현
- **단점**: 테스트 시 목킹 어려움
- **결정**: 초기화 시 테스트 DB 경로 주입 가능하게 설계

---

## 9. 열린 질문
- [ ] 향후 클라우드 동기화 필요 시 아키텍처 변경 범위
- [ ] 키오스크 모드 구현 방식 (별도 윈도우 vs 페이지)
