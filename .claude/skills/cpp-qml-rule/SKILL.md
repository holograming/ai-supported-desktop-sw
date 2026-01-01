---
name: cpp-qml-coding
description: "C++/QML 코딩 컨벤션 및 패턴. 코드 작성/리뷰 시 참조."
---

# C++/QML Coding Standards

## 1. 네이밍 컨벤션

| 타입 | 컨벤션 | 예시 |
|------|--------|------|
| 파일 | snake_case | `user_model.cpp`, `user_model.h` |
| 클래스 | PascalCase | `UserModel`, `DataService` |
| 함수/메서드 | camelCase | `getUserName()`, `fetchData()` |
| 멤버 변수 | m_ prefix + camelCase | `m_userName`, `m_isLoading` |
| 지역 변수 | camelCase | `userName`, `itemCount` |
| 상수 | UPPER_SNAKE | `MAX_ITEMS`, `DEFAULT_TIMEOUT` |
| 네임스페이스 | lowercase | `app::core`, `app::ui` |
| QML 파일 | PascalCase | `UserCard.qml`, `MainPage.qml` |
| QML property | camelCase | `userName`, `isVisible` |

---

## 2. C++ 필수 패턴

### 헤더 파일 구조

```cpp
#pragma once  // ✅ ALWAYS

#include <QObject>
#include <QtQml/qqmlregistration.h>

namespace app::core {  // ✅ 네임스페이스 필수

class UserModel : public QObject
{
    Q_OBJECT
    QML_ELEMENT  // ✅ QML 노출 시
    
    Q_PROPERTY(QString name READ name WRITE setName NOTIFY nameChanged)
    
public:
    explicit UserModel(QObject* parent = nullptr);
    ~UserModel() override = default;
    
    // Getters - const, [[nodiscard]]
    [[nodiscard]] QString name() const { return m_name; }
    
    // Setters
    void setName(const QString& name);
    
    // Q_INVOKABLE - QML에서 호출 가능
    Q_INVOKABLE void refresh();
    
signals:
    void nameChanged();
    void dataLoaded();
    void errorOccurred(const QString& message);
    
private:
    QString m_name;  // m_ prefix
};

} // namespace app::core
```

### 구현 파일 구조

```cpp
#include "user_model.h"

namespace app::core {

UserModel::UserModel(QObject* parent)
    : QObject(parent)
{
}

void UserModel::setName(const QString& name)
{
    if (m_name != name) {
        m_name = name;
        emit nameChanged();  // ✅ 변경 시에만 emit
    }
}

void UserModel::refresh()
{
    // Implementation
}

} // namespace app::core
```

---

## 3. C++ 금지 패턴

```cpp
// ❌ Raw pointer
MyClass* obj = new MyClass();
delete obj;

// ✅ Smart pointer
auto obj = std::make_unique<MyClass>();
// 또는 Qt 스타일
auto* obj = new MyClass(parent);  // parent가 소유권 관리


// ❌ C 스타일 캐스트
int x = (int)floatValue;

// ✅ C++ 캐스트
int x = static_cast<int>(floatValue);


// ❌ 전역 변수
int g_counter = 0;

// ✅ 싱글톤 또는 의존성 주입
class Counter {
public:
    static Counter& instance();
};


// ❌ using namespace in header
using namespace std;  // header에서 금지

// ✅ 명시적 사용
std::string name;
```

---

## 4. QML 필수 패턴

### 컴포넌트 구조

```qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root  // ✅ 항상 id: root
    
    // 1. Properties (public interface)
    required property string userName  // ✅ required for delegates
    property string userEmail: ""
    property bool isSelected: false
    
    // 2. Signals
    signal clicked()
    signal deleteRequested()
    
    // 3. Size hints
    implicitWidth: 300
    implicitHeight: 80
    
    // 4. Child items
    RowLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 16
        
        Label {
            text: root.userName  // ✅ root 참조
            font.bold: true
        }
    }
    
    // 5. Behavior/Animations
    Behavior on opacity {
        NumberAnimation { duration: 200 }
    }
    
    // 6. Handlers
    MouseArea {
        anchors.fill: parent
        onClicked: root.clicked()
    }
}
```

### ListView delegate에서 required property

```qml
ListView {
    model: userModel
    delegate: UserCard {
        // ✅ required property 사용 (모델 역할 자동 주입)
        required property string name
        required property string email
        required property int index
        
        userName: name
        userEmail: email
    }
}
```

---

## 5. QML 금지 패턴

```qml
// ❌ 복잡한 로직을 QML에
function calculateTotal() {
    let sum = 0;
    for (let i = 0; i < items.length; i++) {
        sum += items[i].price * items[i].quantity;
    }
    return sum;
}

// ✅ C++로 이동
// QML: text: backend.totalPrice


// ❌ 하드코딩된 값
Rectangle {
    color: "#FF5722"
    width: 100
    height: 50
}

// ✅ 테마/상수 사용
Rectangle {
    color: Material.accent
    width: Style.buttonWidth
    height: Style.buttonHeight
}


// ❌ 깊은 중첩 (3단계 초과)
Item {
    Column {
        Row {
            Item {
                Column {  // 너무 깊음
                }
            }
        }
    }
}

// ✅ 컴포넌트로 분리
Item {
    Column {
        UserInfoSection { }  // 별도 컴포넌트
        ActionButtons { }
    }
}


// ❌ 바인딩 루프
property int size: width  // width가 size에 의존하면 루프
width: size * 2


// ❌ model 역할 직접 접근 (deprecated)
delegate: Item {
    text: model.name  // ❌ 구식
}

// ✅ required property
delegate: Item {
    required property string name
    text: name
}
```

---

## 6. C++/QML 연동

### Q_PROPERTY 패턴

```cpp
// 읽기 전용
Q_PROPERTY(int count READ count NOTIFY countChanged)

// 읽기/쓰기
Q_PROPERTY(QString name READ name WRITE setName NOTIFY nameChanged)

// 기본값 있는 속성
Q_PROPERTY(bool visible READ isVisible WRITE setVisible NOTIFY visibleChanged)
```

### Signal 네이밍

```cpp
signals:
    // 속성 변경: <property>Changed
    void nameChanged();
    void countChanged();
    
    // 동작 완료: <action>ed, <action>Finished
    void dataLoaded();
    void savingFinished();
    
    // 오류: errorOccurred
    void errorOccurred(const QString& message);
```

### QML_ELEMENT vs qmlRegisterType

```cpp
// ✅ Qt6 방식 - 선언적
class MyClass : public QObject {
    Q_OBJECT
    QML_ELEMENT  // URI는 CMake qt_add_qml_module에서 정의
};

// ❌ 구식 방식
qmlRegisterType<MyClass>("MyApp", 1, 0, "MyClass");
```

---

## 7. CMakeLists.txt 패턴

### QML 모듈 정의

```cmake
qt_add_qml_module(${PROJECT_NAME}
    URI MyApp
    VERSION 1.0
    QML_FILES
        qml/Main.qml
        qml/pages/MainPage.qml
        qml/components/UserCard.qml
    SOURCES
        src/core/user_model.h src/core/user_model.cpp
    RESOURCES
        resources/images/logo.png
)
```

### 소스 추가

```cmake
target_sources(${PROJECT_NAME} PRIVATE
    src/core/user_service.h
    src/core/user_service.cpp
)
```

---

## 8. 에러 처리

### C++

```cpp
// 예외 (권장하지 않음 in Qt)
// Qt는 에러 코드 + signal 패턴 선호

// ✅ Signal로 에러 전달
signals:
    void errorOccurred(const QString& message);
    
void MyClass::doSomething() {
    if (!isValid()) {
        emit errorOccurred(tr("Invalid state"));
        return;
    }
    // ...
}
```

### QML

```qml
Connections {
    target: backend
    function onErrorOccurred(message) {
        errorDialog.text = message
        errorDialog.open()
    }
}
```

---

## 9. 참조 문서

- Qt6 QML Best Practices: https://doc.qt.io/qt-6/qtquick-bestpractices.html
- C++ Integration: https://doc.qt.io/qt-6/qtqml-cppintegration-overview.html
- Property Binding: https://doc.qt.io/qt-6/qtqml-syntax-propertybinding.html
