# 변경: TossPlace POS 앱 Qt/QML 구현

## Status
DEPLOYED

## 이유
토스플레이스 스타일의 POS(Point of Sale) 데스크톱 앱을 Qt6/QML로 구현하여, 직관적이고 세련된 카페 주문/결제 시스템을 구축한다. 샘플 데이터로 카페 메뉴(아메리카노, 라떼 등)를 사용한다.

## 변경 내용
- 새 프로젝트 `toss-pos/` 디렉토리 생성
- Qt 6.5+ / QML / C++17 / CMake 기반 프로젝트 설정
- 토스 디자인 시스템 (색상, 타이포그래피, 컴포넌트)
- SQLite 로컬 데이터베이스 연동
- 상품/카테고리 관리 기능
- 주문 생성 및 관리 기능
- 결제 처리 기능 (시뮬레이션)
- 매출 조회 기능

## 영향
- 영향받는 스펙: **신규 생성** - `specs/toss-pos/spec.md`
- 영향받는 코드: 전체 신규 - `toss-pos/` 디렉토리

## Goal
카페 매장에서 사용할 수 있는 직관적인 POS 앱을 구현한다.
- 상품 등록 및 카테고리 관리
- 터치 친화적인 주문 인터페이스
- 빠른 결제 처리
- 일별/월별 매출 조회

## Scope

### Included
- 프로젝트 설정 (CMake, vcpkg)
- 토스 디자인 시스템 QML 컴포넌트
- 상품/카테고리 CRUD
- 주문 생성 및 장바구니 관리
- 결제 처리 (현금/카드 시뮬레이션)
- 매출 조회 (일별/월별)
- 샘플 데이터 (카페 메뉴)

### Excluded
- 실제 카드 결제 연동 (PG사)
- 재고 관리 시스템
- 다중 사용자/권한 관리
- 프린터 연동 (영수증)
- 클라우드 동기화

## Acceptance Criteria
- [x] 앱이 정상적으로 빌드되고 실행된다
- [x] 카테고리별 상품 목록이 표시된다
- [x] 상품 선택 시 주문 목록에 추가된다
- [x] 주문 총액이 정확히 계산된다
- [x] 결제 완료 시 주문이 저장된다
- [x] 매출 조회 화면에서 매출 내역을 확인할 수 있다
- [x] 토스 디자인 시스템이 일관되게 적용된다

## Design
(architect 에이전트가 추가)

### UI 필요 여부
- [x] UI 작업 필요 (designer 에이전트 호출)
- [ ] UI 작업 불필요

### 수정할 파일
(신규 프로젝트이므로 해당 없음)

### 새 파일
- `toss-pos/CMakeLists.txt`
- `toss-pos/vcpkg.json`
- `toss-pos/main.cpp`
- `toss-pos/qml/Main.qml`
- `toss-pos/qml/theme/TossTheme.qml`
- `toss-pos/qml/components/TossButton.qml`
- `toss-pos/qml/components/ProductCard.qml`
- `toss-pos/qml/pages/OrderPage.qml`
- `toss-pos/qml/pages/PaymentPage.qml`
- `toss-pos/qml/pages/ReportPage.qml`
- `toss-pos/src/models/product_model.h`
- `toss-pos/src/models/product_model.cpp`
- `toss-pos/src/models/order_model.h`
- `toss-pos/src/models/order_model.cpp`
- `toss-pos/src/services/order_service.h`
- `toss-pos/src/services/order_service.cpp`
- `toss-pos/src/database/db_manager.h`
- `toss-pos/src/database/db_manager.cpp`

### 클래스 구조
- DatabaseManager (싱글톤)
  - m_database : QSqlDatabase
  - initialize() : bool
  - getProducts() : QList<Product>
  - saveOrder(Order) : bool

- ProductModel (QAbstractListModel)
  - m_products : QList<Product>
  - m_categoryFilter : QString
  - rowCount() : int
  - data() : QVariant
  - setCategory(QString) : void

- OrderModel (QAbstractListModel)
  - m_items : QList<OrderItem>
  - addItem(Product) : void
  - removeItem(int) : void
  - clear() : void
  - totalAmount() : int

- OrderService
  - m_currentOrder : Order
  - processPayment(PaymentType) : bool
  - getDailyReport(QDate) : Report

## UI Design

### 화면 구조

#### OrderPage (주문 화면) - 메인
- **레이아웃**: 좌측 상품 그리드 (70%) + 우측 주문 패널 (30%)
- **카테고리 바**: 전체/커피/음료/디저트 탭
- **상품 그리드**: 3-5열 (창 크기에 따라), 150x180 카드
- **주문 패널**: 주문 목록 + 총액 + 결제 버튼

#### PaymentPage (결제 화면)
- **중앙 집중 레이아웃**: 결제 금액 + 주문 요약
- **결제 수단 버튼**: 카드/현금 대형 버튼

#### ReportPage (매출 조회)
- **상단**: 일별 매출 요약 카드 (총매출, 주문수, 카드/현금)
- **하단**: 주문 내역 리스트

### 핵심 컴포넌트

| 컴포넌트 | 설명 |
|---------|------|
| TossTheme.qml | 싱글톤 테마 (색상, 폰트, 간격) |
| TossButton.qml | Primary/Secondary/Text 버튼 |
| ProductCard.qml | 상품 카드 (이미지, 이름, 가격) |
| CategoryBar.qml | 카테고리 탭 바 |
| OrderPanel.qml | 주문 목록 패널 |
| OrderItemRow.qml | 주문 항목 행 (수량 +/-) |

### 토스 디자인 시스템

```
Primary Blue: #3182F6
Text Primary: #191F28
Background: #F2F4F6
Surface: #FFFFFF
Success: #03B26C
Error: #F04452
```

### 반응형
- 최소: 1280x720
- 권장: 1920x1080
- 그리드 컬럼 자동 조절 (3-5열)

## Notes
- 토스플레이스 POS 앱의 깔끔한 UI/UX를 참고
- 오프라인 우선 설계 (SQLite 로컬 저장)
- 터치 친화적 인터페이스 고려 (태블릿 확장 대비)
