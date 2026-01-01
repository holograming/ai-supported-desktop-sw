# Capability: TossPlace POS UI 스타일링

## Overview
TossPlace POS 앱의 토스 디자인 시스템 적용 및 한글 렌더링 지원.

## ADDED Requirements

### Requirement: 한글 폰트 지원
앱은 한글 텍스트를 정상적으로 렌더링해야 한다(SHALL).

#### Scenario: macOS에서 한글 표시
- Given: 앱이 macOS에서 실행될 때
- When: 카테고리명, 상품명, 버튼 텍스트 등 한글이 표시될 때
- Then: "Apple SD Gothic Neo" 또는 시스템 기본 한글 폰트로 렌더링된다
- And: 글자 깨짐 없이 정상 표시된다

#### Scenario: Windows에서 한글 표시
- Given: 앱이 Windows에서 실행될 때
- When: 한글 텍스트가 표시될 때
- Then: "Malgun Gothic" 또는 "Noto Sans KR"로 렌더링된다

### Requirement: 토스 디자인 시스템 색상 적용
앱 전체에 토스 디자인 시스템 색상이 일관되게 적용되어야 한다(MUST).

#### Scenario: 배경색 적용
- Given: 앱이 실행될 때
- When: 메인 화면이 표시될 때
- Then: 배경색이 #F2F4F6 (TossTheme.background)로 표시된다

#### Scenario: 카드 컴포넌트 스타일
- Given: 상품 그리드 또는 주문 패널이 표시될 때
- When: 카드 컴포넌트가 렌더링될 때
- Then: 배경색은 #FFFFFF (TossTheme.surface)
- And: 그림자 효과가 적용된다 (DropShadow)
- And: 모서리가 둥글다 (radius: 16px)

#### Scenario: 버튼 색상
- Given: Primary 버튼이 표시될 때
- Then: 배경색은 #3182F6 (TossTheme.primaryBlue)
- And: 텍스트 색상은 #FFFFFF

### Requirement: 카테고리 및 상품 데이터 표시
샘플 데이터가 정상적으로 로드되어 표시되어야 한다(SHALL).

#### Scenario: 카테고리 바 표시
- Given: 주문 페이지가 표시될 때
- When: 카테고리 바가 렌더링될 때
- Then: "전체", "커피", "음료", "디저트", "베이커리" 탭이 표시된다
- And: 기본 선택은 "전체"

#### Scenario: 상품 그리드 표시
- Given: "전체" 카테고리가 선택된 상태에서
- When: 상품 그리드가 렌더링될 때
- Then: 모든 카테고리의 상품이 표시된다
- And: 각 상품에 이름과 가격이 표시된다
- And: 가격은 "원" 단위로 포맷된다 (예: "4,500원")

### Requirement: 카드 그림자 효과
TossCard 컴포넌트에 그림자 효과가 적용되어야 한다(SHALL).

#### Scenario: 그림자 렌더링
- Given: TossCard 컴포넌트가 사용될 때
- When: 카드가 렌더링될 때
- Then: 하단과 우측에 부드러운 그림자가 표시된다
- And: 그림자 색상은 반투명 검정 (약 10% 불투명도)
- And: 그림자 blur 반경은 8-12px

### Requirement: UTF-8 인코딩 지원
소스 코드 내 한글 문자열이 올바르게 컴파일되어야 한다(MUST).

#### Scenario: 한글 문자열 컴파일
- Given: C++ 소스 코드에 한글 문자열이 포함될 때
- When: 프로젝트가 빌드될 때
- Then: 한글이 UTF-8로 올바르게 인코딩된다
- And: 런타임에 한글이 깨지지 않는다

## Cross-references
- `add-toss-pos-app` proposal의 디자인 섹션 참조
- 토스 디자인 시스템: Primary Blue #3182F6, Background #F2F4F6
