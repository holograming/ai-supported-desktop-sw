# Tasks: TossPlace POS UI 스타일링 수정

## 우선순위 높음 (P0) - 핵심 문제 해결

### T1. UTF-8 컴파일 설정 추가
- [x] CMakeLists.txt에 UTF-8 인코딩 컴파일 옵션 추가
- 검증: 빌드 성공, 한글 문자열 정상 컴파일

### T2. 한글 폰트 설정
- [x] main.cpp에 QFont 설정 추가
- [x] 플랫폼별 폰트 분기 (macOS: Apple SD Gothic Neo, Windows: Malgun Gothic)
- 검증: 앱 실행 시 한글 정상 렌더링

### T3. TossTheme 싱글톤 로드 확인
- [x] QML 파일들의 import 경로 검토
- [x] 필요시 import 방식 수정 (상대경로 → 모듈 import)
- 검증: TossTheme 속성 (background, primaryBlue 등) 정상 적용

### T4. 데이터베이스 데이터 확인
- [x] SQLite DB에 카테고리/상품 데이터 확인
- [x] 필요시 DatabaseManager 초기화 로직 수정
- 검증: 카테고리 바에 한글 카테고리명 표시, 상품 그리드에 상품 표시

## 우선순위 중간 (P1) - 디자인 완성도

### T5. DropShadow 효과 추가
- [x] TossCard.qml에 그림자 효과 구현 (Rectangle 기반 시뮬레이션)
- 검증: 카드 컴포넌트에 그림자 표시

### T6. 폰트 패밀리 속성 추가
- [x] TossTheme.qml에 fontFamily 속성 추가
- 검증: 일관된 폰트 사용

## 우선순위 낮음 (P2) - 선택 개선

### T7. 페이지 전환 애니메이션 (선택)
- [ ] Main.qml StackView에 pushEnter/pushExit/popEnter/popExit 설정
- 검증: 페이지 이동 시 부드러운 전환
- *미구현 - 향후 개선 사항*

### T8. 리스트 애니메이션 (선택)
- [ ] OrderPanel의 ListView에 add/remove Transition 추가
- 검증: 주문 항목 추가/삭제 시 애니메이션
- *미구현 - 향후 개선 사항*

## 검증 단계

### V1. 빌드 검증
- [x] macOS에서 빌드 성공
- [x] 빌드 경고 없음 (minor CMake 경고 제외)

### V2. 시각적 검증
- [x] 배경색 #F2F4F6 확인
- [x] 카테고리 바 정상 표시
- [x] 상품 그리드 정상 표시
- [x] 카드 그림자 확인
- [x] 한글 폰트 정상

### V3. 기능 검증
- [x] 상품 클릭 시 주문 추가
- [x] 결제 버튼 동작
- [x] 주문 목록 표시 정상

## 추가 수정 사항 (런타임 오류 해결)

### T9. QML_ELEMENT 싱글톤 충돌 해결
- [x] CategoryModel, ProductModel, OrderModel에서 QML_ELEMENT 매크로 제거
- [x] OrderService, ReportService에서 QML_ELEMENT 매크로 제거
- 원인: QML_ELEMENT로 컴파일 타임 등록 + qmlRegisterSingletonInstance() 런타임 등록 충돌
- 검증: `TypeError: was not a singleton at compile time` 오류 해결

### T10. QML import 경로 수정
- [x] main.cpp에 `engine.addImportPath("qrc:/")` 추가
- 검증: PaymentPage, ReportPage 로드 정상

### T11. ProductCard delegate 바인딩 수정
- [x] ProductCard.qml에서 required property 유지
- [x] OrderPage.qml delegate에서 중복 required property 선언 제거
- 원인: 모델 role 데이터가 delegate를 통해 ProductCard에 전달되지 않음
- 검증: 상품 그리드에 20개 상품 정상 표시

### T12. OrderItemRow delegate 바인딩 수정
- [x] OrderPanel.qml delegate에서 중복 required property 선언 제거
- 원인: 모델 role 데이터가 OrderItemRow에 전달되지 않음
- 검증: 주문 목록에 상품명, 수량, 가격 정상 표시

## 완료된 수정 사항

| 파일 | 수정 내용 |
|------|----------|
| `toss-pos/CMakeLists.txt` | UTF-8 컴파일 옵션, Qt5Compat 설정 추가 |
| `toss-pos/main.cpp` | 한글 폰트 설정, Basic 스타일, QML import 경로 추가 |
| `toss-pos/qml/theme/TossTheme.qml` | fontFamily 속성 추가 |
| `toss-pos/qml/components/TossCard.qml` | Rectangle 기반 그림자 효과 구현 |
| `toss-pos/qml/components/ProductCard.qml` | required property → 일반 property 변경 |
| `toss-pos/qml/Main.qml` | 상대 경로 import 제거 |
| `toss-pos/qml/pages/OrderPage.qml` | delegate required property 바인딩 수정 |
| `toss-pos/qml/pages/*.qml` | 상대 경로 import 제거 |
| `toss-pos/qml/components/*.qml` | 상대 경로 import 수정 (모듈 import 사용) |
| `toss-pos/src/models/*.h` | QML_ELEMENT 매크로 제거 (싱글톤 충돌 해결) |
| `toss-pos/src/services/*.h` | QML_ELEMENT 매크로 제거 (싱글톤 충돌 해결) |
| `toss-pos/qml/components/OrderPanel.qml` | delegate 중복 required property 제거 |
