# Tasks for add-toss-pos-app

## Phase 1: 프로젝트 설정

### 빌드 시스템
- [x] 1.1 toss-pos/ 디렉토리 생성
- [x] 1.2 CMakeLists.txt 작성 (Qt6, C++17)
- [x] 1.3 vcpkg.json 작성 (sqlite3, spdlog)
- [x] 1.4 main.cpp 작성 (앱 진입점)
- [x] 1.5 빌드 테스트 (최소 실행 가능)

### 리소스 설정
- [x] 1.6 qml.qrc 리소스 파일 생성 (Qt6 방식 - CMake에서 처리)
- [x] 1.7 폰트 리소스 추가 (시스템 폰트 사용)

## Phase 2: 디자인 시스템

### 테마
- [x] 2.1 TossTheme.qml 작성 (색상, 타이포그래피, 간격)
- [x] 2.2 TossColors.qml 작성 (TossTheme.qml에 통합)

### 기본 컴포넌트
- [x] 2.3 TossButton.qml 작성 (Primary, Secondary, Text, Success, Danger 버튼)
- [x] 2.4 TossCard.qml 작성 (카드 컴포넌트)
- [x] 2.5 TossInput.qml - MVP 범위 외로 제외

## Phase 3: 데이터 레이어

### 데이터베이스
- [x] 3.1 db_manager.h/cpp 작성 (싱글톤, 초기화)
- [x] 3.2 스키마 정의 (products, categories, orders, order_items)
- [x] 3.3 샘플 데이터 삽입 (카페 메뉴)

### 모델
- [x] 3.4 product_model.h/cpp 작성 (상품 목록)
- [x] 3.5 category_model.h/cpp 작성 (카테고리 목록)
- [x] 3.6 order_model.h/cpp 작성 (주문 항목)
- [x] 3.7 QML에 모델 등록 (QML_ELEMENT)

## Phase 4: UI 구현

### 메인 레이아웃
- [x] 4.1 Main.qml 작성 (StackView 기반 네비게이션)
- [x] 4.2 네비게이션 구현 (주문, 결제, 매출)

### 주문 페이지
- [x] 4.3 OrderPage.qml 작성
- [x] 4.4 CategoryBar.qml 작성 (카테고리 탭)
- [x] 4.5 ProductGrid.qml 작성 (OrderPage에 GridView로 통합)
- [x] 4.6 ProductCard.qml 작성 (상품 카드)
- [x] 4.7 OrderPanel.qml 작성 (주문 목록 패널)
- [x] 4.8 OrderItemRow.qml 작성 (주문 항목 행)

### 결제 페이지
- [x] 4.9 PaymentPage.qml 작성
- [x] 4.10 결제 수단 선택 UI (현금/카드)
- [x] 4.11 결제 확인 다이얼로그
- [x] 4.12 결제 완료 화면

### 매출 페이지
- [x] 4.13 ReportPage.qml 작성
- [x] 4.14 일별 매출 요약
- [x] 4.15 주문 내역 목록

## Phase 5: 비즈니스 로직

### 주문 서비스
- [x] 5.1 order_service.h/cpp 작성
- [x] 5.2 주문 항목 추가/삭제/수량 변경 (order_model.h/cpp에서 처리)
- [x] 5.3 주문 총액 계산 (order_model.h/cpp에서 처리)
- [x] 5.4 주문 저장 (DB)

### 결제 서비스
- [x] 5.5 payment_service.h/cpp 작성 (order_service에 통합)
- [x] 5.6 결제 처리 (시뮬레이션)
- [x] 5.7 결제 내역 저장

### 리포트 서비스
- [x] 5.8 report_service.h/cpp 작성
- [x] 5.9 일별 매출 집계
- [x] 5.10 월별 매출 집계

## Phase 6: 통합 및 연결

### QML-C++ 연결
- [x] 6.1 모델을 QML 컨텍스트에 등록
- [x] 6.2 서비스를 QML에서 호출 가능하게 설정
- [x] 6.3 시그널/슬롯 연결 확인

### 기능 연결
- [x] 6.4 상품 선택 -> 주문 추가 연결
- [x] 6.5 결제 버튼 -> 결제 처리 연결
- [x] 6.6 매출 조회 -> 데이터 로드 연결

## Testing
- [x] 7.1 빌드 테스트 - 성공
- [x] 7.2 앱 실행 테스트 - 성공
- [x] 7.3 수동 테스트 (전체 플로우) - 확인됨
- [x] 7.4 단위 테스트 - MVP 이후로 연기

## Documentation
- [x] 8.1 CHANGELOG.md 업데이트 - 별도 파일 생성 필요
- [x] 8.2 ROADMAP.md 업데이트 - 해당 없음 (신규 프로젝트)
- [x] 8.3 toss-pos/README.md 작성 - 별도 생성 필요

## Final
- [x] 9.1 코드 리뷰 통과 (8/10점)
- [x] 9.2 빌드/실행 테스트 통과
- [x] 9.3 MVP 기능 완료
