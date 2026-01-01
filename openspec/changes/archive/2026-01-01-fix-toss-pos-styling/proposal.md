# 변경: TossPlace POS UI 스타일링 수정

## Status
COMPLETE

## Why
TossPlace POS 앱의 1차 개발이 완료되었으나, 실행 결과 토스 디자인 시스템이 제대로 적용되지 않았다.
스크린샷에서 확인된 문제: 한글 폰트 깨짐, 배경색 미적용, 제품 그리드 비어있음, 카테고리 텍스트 깨짐.

## 문제 분석 (팀 논의 결과)

### 아키텍트 (도산) 분석
1. **한글 폰트 설정 누락**: main.cpp에 폰트 패밀리 설정 없음
2. **TossTheme 싱글톤 로드 문제**: QML import 경로 문제 가능성
3. **UTF-8 인코딩 문제**: C++ 소스 내 한글 문자열 컴파일 시 깨질 수 있음
4. **데이터베이스 초기화 확인 필요**: 카테고리/상품 데이터 로드 문제

### 디자이너 (사하) 분석
1. **디자인 시스템 코드는 구현됨**: TossTheme.qml에 색상, 간격, 폰트 크기 정의됨
2. **TossCard 그림자 효과 누락**: DropShadow 미구현으로 평면적 외관
3. **폰트 패밀리 미정의**: 시스템 기본 폰트 사용 중
4. **근본 원인**: TossTheme 싱글톤이 QML에서 제대로 로드되지 않음

## What Changes

### 필수 수정
1. main.cpp에 한글 폰트 설정 추가 (Apple SD Gothic Neo / Noto Sans KR)
2. CMakeLists.txt에 UTF-8 컴파일 옵션 추가
3. TossCard.qml에 DropShadow 효과 추가
4. TossTheme.qml에 폰트 패밀리 속성 추가
5. QML import 경로 정리 및 확인

### 선택 수정
- 페이지 전환 애니메이션 추가
- 리스트 추가/삭제 애니메이션 추가

## 영향
- 영향받는 스펙: `specs/toss-pos/spec.md` (향후 생성)
- 영향받는 코드:
  - `toss-pos/main.cpp`
  - `toss-pos/CMakeLists.txt`
  - `toss-pos/qml/theme/TossTheme.qml`
  - `toss-pos/qml/components/TossCard.qml`

## Goal
토스 디자인 시스템이 일관되게 적용된 세련된 POS UI 완성
- 한글 폰트가 정상적으로 렌더링됨
- 배경색, 카드 그림자 등 토스 스타일 적용
- 상품/카테고리 데이터가 정상 표시됨

## Scope

### Included
- 폰트 설정 (한글 지원)
- UTF-8 인코딩 수정
- TossTheme 싱글톤 로드 문제 해결
- TossCard 그림자 효과 구현
- 디버깅 및 검증

### Excluded
- 새 기능 추가
- 데이터 구조 변경
- 테스트 코드 추가

## Acceptance Criteria
- [x] 앱 실행 시 한글이 정상적으로 표시된다
- [x] 배경색이 #F2F4F6으로 표시된다
- [x] 카테고리 바에 "전체", "커피", "음료", "디저트", "베이커리"가 표시된다
- [x] 상품 그리드에 샘플 상품들이 표시된다
- [x] 카드 컴포넌트에 그림자 효과가 보인다
- [x] 토스 디자인 시스템 색상이 일관되게 적용된다
- [x] 주문 목록에 상품명, 수량, 가격이 표시된다

## Design

### 수정할 파일
| 파일 | 수정 내용 |
|------|----------|
| `toss-pos/main.cpp` | 한글 폰트 설정 추가 |
| `toss-pos/CMakeLists.txt` | UTF-8 컴파일 옵션, GraphicalEffects 모듈 추가 |
| `toss-pos/qml/theme/TossTheme.qml` | 폰트 패밀리 속성 추가 |
| `toss-pos/qml/components/TossCard.qml` | DropShadow 효과 구현 |

### 폰트 설정 방안
```cpp
// macOS
font.setFamily("Apple SD Gothic Neo");
// Windows
font.setFamily("Malgun Gothic");
// Fallback
font.setFamily("Noto Sans KR");
```

### 그림자 효과 방안
Qt6에서는 두 가지 방법 가능:
1. **Qt5Compat.GraphicalEffects**: `DropShadow` 사용 (호환성 좋음)
2. **MultiEffect**: Qt 6.5+ 네이티브 (성능 좋음)

권장: Qt5Compat.GraphicalEffects 사용 (안정성)

## Notes
- 이 수정은 코드 구조 변경 없이 스타일링만 수정
- 빌드 후 반드시 실행하여 시각적 검증 필요
- macOS와 Windows에서 모두 테스트 권장
