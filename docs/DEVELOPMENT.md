# TossPlace POS - 신규 개발자 온보딩 가이드

이 문서는 TossPlace POS 프로젝트에 신규 개발자가 빠르게 시작할 수 있도록 돕기 위한 가이드입니다.

## 📋 목차

1. [개발 환경 준비](#개발-환경-준비)
2. [첫 빌드](#첫-빌드)
3. [프로젝트 구조](#프로젝트-구조)
4. [개발 워크플로우](#개발-워크플로우)
5. [코드 스타일](#코드-스타일)
6. [일반적인 작업](#일반적인-작업)
7. [팀 규칙](#팀-규칙)

---

## 개발 환경 준비

### 사전 결정: 브랜치 선택

이 프로젝트는 두 가지 브랜치 전략을 제공합니다:

| 기준 | main 브랜치 | windows 브랜치 |
|------|------------|---------------|
| **저장소 크기** | 50MB 미만 | 500MB+ |
| **설치 시간** | 5-10분 | 1-2분 (submodule로 인해 클론이 느림) |
| **플랫폼** | 모든 플랫폼 | Windows 권장 |
| **vcpkg 방식** | 자동 다운로드 | Git submodule (포함) |
| **네트워크** | 필수 (처음 빌드 시) | 첫 클론 시에만 필요 |
| **개발 환경** | 가볍고 빠름 | 무겁지만 더 자동화됨 |

**권장**:
- 대부분의 개발자: **main** 브랜치
- Windows 주요 개발자: **windows** 브랜치

자세한 내용은 [BRANCHING.md](BRANCHING.md)를 참고하세요.

### 0분: 시스템 요구사항 확인

**모든 개발자:**
- CMake 4.2.0 이상
- Git 최신 버전
- 인터넷 연결 (처음 빌드 시 의존성 다운로드)

**Windows:**
- Windows 10 이상
- Visual Studio 2022 Community (무료) 이상
  - [다운로드](https://visualstudio.microsoft.com/vs/)
  - 설치 시 **"Desktop development with C++"** 워크로드 선택

**macOS:**
- macOS 10.15 이상 (Intel) 또는 11.0 이상 (Apple Silicon)
- Xcode Command Line Tools
  ```bash
  xcode-select --install
  ```

### 10분: 저장소 복제

```bash
git clone https://github.com/your-org/toss-pos.git
cd toss-pos
```

### 5분: 개발 환경 자동 설정

**Windows:**
```bash
.\build-scripts\setup-dev.bat
```

**macOS/Linux:**
```bash
./build-scripts/setup-dev.sh
source ~/.bashrc  # 또는 ~/.zshrc
```

스크립트가 자동으로:
- vcpkg 설치 (또는 기존 설치 감지)
- 환경 변수 설정
- 완료 메시지 출력

### 2-3시간: 첫 빌드

**Windows:**
```bash
cd toss-pos
cmake --preset windows-x64
cmake --build --preset windows-release
```

**macOS Intel:**
```bash
cd toss-pos
cmake --preset macos-x64
cmake --build --preset macos-x64
```

**macOS ARM64 (M1/M2/M3):**
```bash
cd toss-pos
cmake --preset macos-arm64
cmake --build --preset macos-arm64
```

> **⏰ 처음 빌드는 30-60분이 걸립니다!**
> Qt 6.5가 처음 컴파일되기 때문입니다. 이후 빌드는 캐시로 5-10분 정도 소요됩니다.

---

## 첫 빌드

### 앱 실행

**Windows:**
```bash
.\build\windows-x64\toss-pos.exe
```

**macOS:**
```bash
./build/macos-x64/toss-pos      # Intel
./build/macos-arm64/toss-pos    # ARM64
```

### 예상 결과

앱이 다음과 같이 표시되어야 합니다:
- 메인 윈도우 (토스 디자인 시스템 색상)
- 좌측: 카테고리 탭 (커피, 음료, 디저트 등)
- 중앙: 상품 그리드
- 우측: 주문 패널 (카드 스타일, 그림자 효과)
- 상단: 매출 리포트 탭

---

## 프로젝트 구조

```
toss-pos/
├── CMakeLists.txt               # CMake 빌드 설정
├── CMakePresets.json            # 플랫폼별 빌드 preset
├── main.cpp                     # 앱 진입점
├── vcpkg.json                   # 의존성 선언
├── vcpkg-configuration.json     # vcpkg baseline 설정
│
├── qml/                         # UI 레이어 (QML)
│   ├── Main.qml               # 루트 윈도우
│   ├── pages/                 # 페이지 컴포넌트
│   │   ├── OrderPage.qml
│   │   ├── PaymentPage.qml
│   │   └── ReportPage.qml
│   ├── components/            # 재사용 컴포넌트
│   │   ├── TossButton.qml
│   │   ├── TossCard.qml
│   │   ├── ProductCard.qml
│   │   └── ...
│   └── theme/                 # 디자인 시스템
│       └── TossTheme.qml
│
├── src/                         # 비즈니스 로직 (C++)
│   ├── models/                # 데이터 모델
│   │   ├── category_model.cpp
│   │   ├── product_model.cpp
│   │   └── order_model.cpp
│   ├── services/              # 비즈니스 로직 서비스
│   │   ├── order_service.cpp
│   │   └── report_service.cpp
│   ├── database/              # 데이터 액세스
│   │   └── db_manager.cpp
│   └── types/                 # 도메인 타입
│       ├── product.h
│       └── order.h
│
├── resources/                   # 리소스 파일
│   └── sample_data.sql
│
├── build/                       # 빌드 결과 (플랫폼별)
│   ├── windows-x64/
│   ├── macos-x64/
│   └── macos-arm64/
│
└── docs/                        # 문서
    ├── BUILD.md               # 빌드 가이드 (이 파일)
    └── DEVELOPMENT.md         # 개발자 온보딩
```

### 핵심 개념

- **QML**: Qt Quick Language - 선언형 UI 정의
- **Model-View 패턴**: `CategoryModel`, `ProductModel` 등
- **Service 레이어**: `OrderService`, `ReportService`
- **Singleton**: `DatabaseManager`, `TossTheme`

---

## 개발 워크플로우

### 1. 기능 개발

```bash
# 1. 기능 브랜치 생성
git checkout -b feature/새기능

# 2. 코드 작성 (QML 또는 C++)

# 3. 로컬 빌드 및 테스트
cmake --build --preset <preset>
./build/<preset>/toss-pos

# 4. 변경사항 커밋
git add .
git commit -m "feat: 새로운 기능 설명"

# 5. 푸시 및 PR 생성
git push origin feature/새기능
```

### 2. 버그 수정

```bash
# 1. 버그 브랜치 생성
git checkout -b fix/버그설명

# 2. 코드 수정 및 테스트

# 3. 커밋
git commit -m "fix: 버그 설명"

# 4. 푸시 및 PR
git push origin fix/버그설명
```

### 3. 코드 리뷰

PR이 머지되려면:
- [ ] 코드 리뷰 승인 (영실)
- [ ] CI 빌드 성공 (지평)
- [ ] 테스트 통과

---

## 코드 스타일

### C++

**명명 규칙:**
```cpp
class OrderModel { };              // PascalCase
void processPayment() { }          // camelCase
int m_totalAmount;                 // m_ 접두사 (멤버 변수)
```

**파일명:**
```
order_model.cpp                    // snake_case
product_service.h
```

**들여쓰기:**
```cpp
// 4칸 스페이스 (탭 금지)
void MyFunction() {
    if (condition) {
        doSomething();
    }
}
```

### QML

**컴포넌트 명명:**
```qml
Rectangle {
    id: orderPanel                 // camelCase
    color: TossTheme.surface
}
```

**파일명:**
```
OrderPanel.qml                     // PascalCase
TossButton.qml
ProductCard.qml
```

---

## 일반적인 작업

### 새로운 QML 컴포넌트 추가

1. `qml/components/MyComponent.qml` 생성
2. `CMakeLists.txt`의 `qt_add_qml_module`에 추가
3. 다른 QML 파일에서 import 및 사용

```qml
// qml/components/MyButton.qml
import QtQuick
import TossPos

Button {
    text: "My Button"
    onClicked: {
        console.log("Clicked!")
    }
}
```

### 새로운 C++ 모델 추가

1. `src/models/my_model.h/cpp` 생성
2. `QAbstractListModel` 상속
3. `CMakeLists.txt`에 파일 추가
4. `qt_add_qml_module`의 `SOURCES`에 추가

```cpp
// src/models/my_model.h
#pragma once
#include <QAbstractListModel>

class MyModel : public QAbstractListModel {
    Q_OBJECT
public:
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;
    // ... 구현
};
```

### 데이터베이스 쿼리 추가

1. `src/database/db_manager.cpp`에 메서드 추가
2. SQL 쿼리 작성
3. 결과를 도메인 타입(`Product`, `Order` 등)으로 변환

```cpp
// src/database/db_manager.cpp
QList<Product> DatabaseManager::getProductsByCategory(const QString &category) {
    QList<Product> products;
    QSqlQuery query;
    query.prepare("SELECT * FROM products WHERE category = ?");
    query.addBindValue(category);

    if (query.exec()) {
        while (query.next()) {
            Product p;
            p.id = query.value("id").toInt();
            p.name = query.value("name").toString();
            // ... 파싱
            products.append(p);
        }
    }
    return products;
}
```

---

## 팀 규칙

### 커밋 메시지

[Conventional Commits](https://www.conventionalcommits.org/) 형식:

```
feat: 새로운 기능 추가
fix: 버그 수정
refactor: 코드 리팩토링 (기능 변화 없음)
test: 테스트 추가
docs: 문서 수정
style: 코드 스타일 (들여쓰기, 세미콜론 등)
chore: 빌드 설정, 의존성 관리
```

**예시:**
```
feat: 결제 페이지에 신용카드 결제 옵션 추가

- Stripe API 통합
- 카드 정보 암호화
- 영수증 생성 기능
```

### 브랜치 네이밍

```
feature/새기능           # 새로운 기능
fix/버그설명            # 버그 수정
refactor/기능개선        # 코드 개선
docs/문서업데이트        # 문서 작성/수정
```

### 빌드 성공 확인

모든 플랫폼에서 빌드해야 합니다:

```bash
# Windows
cmake --preset windows-x64
cmake --build --preset windows-release

# macOS Intel
cmake --preset macos-x64
cmake --build --preset macos-x64

# macOS ARM64 (가능한 경우)
cmake --preset macos-arm64
cmake --build --preset macos-arm64
```

### 코드 리뷰 체크리스트

PR 생성 시 다음을 확인하세요:
- [ ] 코드 스타일 준수 (C++ / QML)
- [ ] 모든 플랫폼에서 빌드 성공
- [ ] 기본적인 기능 테스트 완료
- [ ] 불필요한 파일 제거 (`.o`, `.exe` 등)
- [ ] 커밋 메시지 명확

---

## 도움말 및 리소스

### 내부 문서

- [빌드 가이드](BUILD.md) - 상세한 빌드 지침
- [프로젝트 규칙](../openspec/project.md) - 아키텍처 및 규칙

### 외부 리소스

- [Qt 6 공식 문서](https://doc.qt.io/qt-6/)
- [CMake 공식 문서](https://cmake.org/cmake/help/latest/)
- [vcpkg 가이드](https://github.com/Microsoft/vcpkg)
- [C++17 표준](https://en.cppreference.com/)

### 질문하기

팀의 연락처:
- **아키텍트** (도산): 설계 관련 질문
- **DevOps** (인재): 빌드/배포 관련 질문
- **코드 리뷰어** (영실): 코드 스타일 질문

---

**Welcome to TossPlace POS! 🚀**

행운을 빕니다! 혹시 막히는 부분이 있으면 팀에 물어보세요.
