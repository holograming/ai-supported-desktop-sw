---
name: qml-desktop-ui
description: "QML + C++ Desktop UI 앱 개발 가이드. CMake 프로젝트 설정, C++ 백엔드 연동, Model-View 데이터 바인딩, 스타일링, 배포. Qt Quick Controls 기반 데스크톱 앱 생성 시 사용."
---

# QML Desktop UI

QML + C++ Desktop 앱 개발 핵심 가이드.

## When to Use

**Apply this skill when:**
- Qt Quick Desktop 앱 프로젝트 생성
- CMake + qt_add_qml_module 설정
- C++ 타입을 QML에 노출 (QML_ELEMENT, Q_PROPERTY)
- ListView/Model-View 데이터 바인딩
- 앱 배포 (windeployqt, macdeployqt)

**Do NOT apply when:**
- 모바일 전용 UI (SwipeView, Drawer)
- Qt Widgets 앱 (QMainWindow, QDialog)
- QML 없는 순수 C++ Qt 앱

## 1. 프로젝트 구조

```
myapp/
├── CMakeLists.txt
├── main.cpp
├── qml/
│   ├── Main.qml
│   └── components/
├── src/
│   ├── models/          # C++ 모델
│   └── controllers/     # C++ 컨트롤러
├── images/
└── qtquickcontrols2.conf
```

### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.16)
project(myapp VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 6.5 REQUIRED COMPONENTS Quick QuickControls2)
qt_standard_project_setup(REQUIRES 6.5)

qt_add_executable(myapp main.cpp)

qt_add_qml_module(myapp
    URI MyApp
    VERSION 1.0
    QML_FILES
        qml/Main.qml
    RESOURCES
        images/logo.png
        qtquickcontrols2.conf
    SOURCES
        src/models/contactmodel.h src/models/contactmodel.cpp
)

target_link_libraries(myapp PRIVATE Qt6::Quick Qt6::QuickControls2)

# 배포
install(TARGETS myapp BUNDLE DESTINATION . RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
qt_generate_deploy_qml_app_script(TARGET myapp OUTPUT_SCRIPT deploy_script)
install(SCRIPT ${deploy_script})
```

### main.cpp

```cpp
#include <QGuiApplication>
#include <QQmlApplicationEngine>

int main(int argc, char *argv[]) {
    QGuiApplication app(argc, argv);
    QQmlApplicationEngine engine;
    engine.loadFromModule("MyApp", "Main");
    return app.exec();
}
```

## 2. 데이터 & 모델

### QML ListModel

```qml
ListView {
    model: ListModel {
        ListElement { name: "Alice"; age: 30 }
        ListElement { name: "Bob"; age: 25 }
    }
    delegate: ItemDelegate {
        required property string name  // ✅ required properties 사용
        required property int age
        required property int index
        text: `${index}: ${name} (${age})`
    }
}
```

### C++ Model (QAbstractListModel)

```cpp
// contactmodel.h
#include <QAbstractListModel>
#include <QtQml/qqmlregistration.h>

class ContactModel : public QAbstractListModel {
    Q_OBJECT
    QML_ELEMENT  // ✅ qmlRegisterType() 대신 선언적 등록

    enum Roles { NameRole = Qt::UserRole + 1, EmailRole };

public:
    int rowCount(const QModelIndex &parent = {}) const override;
    QVariant data(const QModelIndex &index, int role) const override;
    QHash<int, QByteArray> roleNames() const override {
        return {{NameRole, "name"}, {EmailRole, "email"}};
    }

    Q_INVOKABLE void addContact(const QString &name, const QString &email);

private:
    struct Contact { QString name, email; };
    QList<Contact> m_contacts;
};
```

```qml
// Main.qml
import MyApp

ListView {
    model: ContactModel {}
    delegate: ItemDelegate {
        required property string name
        required property string email
        text: `${name} <${email}>`
    }
}
```

## 3. C++ 백엔드 연동

```cpp
// backend.h
class Backend : public QObject {
    Q_OBJECT
    QML_ELEMENT
    Q_PROPERTY(QString status READ status WRITE setStatus NOTIFY statusChanged)

public:
    QString status() const { return m_status; }
    void setStatus(const QString &s) {
        if (m_status != s) { m_status = s; emit statusChanged(); }
    }

    Q_INVOKABLE void doSomething() { setStatus("Done"); }

signals:
    void statusChanged();

private:
    QString m_status;
};
```

```qml
Backend {
    id: backend
    onStatusChanged: console.log("Status:", status)
}
Button { onClicked: backend.doSomething() }
```

## 4. 스타일 & 테마

### qtquickcontrols2.conf

```ini
[Controls]
Style=Fusion

[Fusion]
; 또는 Material, Universal, Basic
```

### 런타임 스타일 지정

```cpp
// main.cpp
QQuickStyle::setStyle("Material");
```

```qml
// Material 테마 커스터마이징
import QtQuick.Controls.Material
ApplicationWindow {
    Material.theme: Material.Dark
    Material.accent: Material.Purple
}
```

## 5. 배포

### CMake 배포 스크립트

```cmake
qt_generate_deploy_qml_app_script(
    TARGET myapp
    OUTPUT_SCRIPT deploy_script
)
install(SCRIPT ${deploy_script})
```

### 수동 배포

```bash
# Windows
windeployqt --qmldir ./qml ./build/myapp.exe

# macOS
macdeployqt ./build/myapp.app -qmldir=./qml
```

## References

- [Qt Quick Controls](https://doc.qt.io/qt-6/qtquickcontrols-index.html)
- [qt_add_qml_module](https://doc.qt.io/qt-6/qt-add-qml-module.html)
- [Model-View](https://doc.qt.io/qt-6/qtquick-modelviewsdata-modelview.html)
- [C++ Integration](https://doc.qt.io/qt-6/qtqml-cppintegration-overview.html)
- [Deployment](https://doc.qt.io/qt-6/cmake-deployment.html)
- [Best Practices](https://doc.qt.io/qt-6/qtquick-bestpractices.html)
