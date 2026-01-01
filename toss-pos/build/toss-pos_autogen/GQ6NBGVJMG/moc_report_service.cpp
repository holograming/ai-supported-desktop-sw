/****************************************************************************
** Meta object code from reading C++ file 'report_service.h'
**
** Created by: The Qt Meta Object Compiler version 69 (Qt 6.9.0)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../../src/services/report_service.h"
#include <QtCore/qmetatype.h>

#include <QtCore/qtmochelpers.h>

#include <memory>


#include <QtCore/qxptype_traits.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'report_service.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 69
#error "This file was generated using the moc from 6.9.0. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

#ifndef Q_CONSTINIT
#define Q_CONSTINIT
#endif

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
QT_WARNING_DISABLE_GCC("-Wuseless-cast")
namespace {
struct qt_meta_tag_ZN7tosspos13ReportServiceE_t {};
} // unnamed namespace

template <> constexpr inline auto tosspos::ReportService::qt_create_metaobjectdata<qt_meta_tag_ZN7tosspos13ReportServiceE_t>()
{
    namespace QMC = QtMocConstants;
    QtMocHelpers::StringRefStorage qt_stringData {
        "tosspos::ReportService",
        "QML.Element",
        "auto",
        "currentDateChanged",
        "",
        "reportChanged",
        "refresh",
        "goToToday",
        "previousDay",
        "nextDay",
        "formatDate",
        "date",
        "getMonthlyReport",
        "QVariantList",
        "year",
        "month",
        "currentDate",
        "totalSales",
        "orderCount",
        "cashSales",
        "cardSales",
        "orders"
    };

    QtMocHelpers::UintData qt_methods {
        // Signal 'currentDateChanged'
        QtMocHelpers::SignalData<void()>(3, 4, QMC::AccessPublic, QMetaType::Void),
        // Signal 'reportChanged'
        QtMocHelpers::SignalData<void()>(5, 4, QMC::AccessPublic, QMetaType::Void),
        // Method 'refresh'
        QtMocHelpers::MethodData<void()>(6, 4, QMC::AccessPublic, QMetaType::Void),
        // Method 'goToToday'
        QtMocHelpers::MethodData<void()>(7, 4, QMC::AccessPublic, QMetaType::Void),
        // Method 'previousDay'
        QtMocHelpers::MethodData<void()>(8, 4, QMC::AccessPublic, QMetaType::Void),
        // Method 'nextDay'
        QtMocHelpers::MethodData<void()>(9, 4, QMC::AccessPublic, QMetaType::Void),
        // Method 'formatDate'
        QtMocHelpers::MethodData<QString(const QDate &) const>(10, 4, QMC::AccessPublic, QMetaType::QString, {{
            { QMetaType::QDate, 11 },
        }}),
        // Method 'getMonthlyReport'
        QtMocHelpers::MethodData<QVariantList(int, int) const>(12, 4, QMC::AccessPublic, 0x80000000 | 13, {{
            { QMetaType::Int, 14 }, { QMetaType::Int, 15 },
        }}),
    };
    QtMocHelpers::UintData qt_properties {
        // property 'currentDate'
        QtMocHelpers::PropertyData<QDate>(16, QMetaType::QDate, QMC::DefaultPropertyFlags | QMC::Writable | QMC::StdCppSet, 0),
        // property 'totalSales'
        QtMocHelpers::PropertyData<int>(17, QMetaType::Int, QMC::DefaultPropertyFlags, 1),
        // property 'orderCount'
        QtMocHelpers::PropertyData<int>(18, QMetaType::Int, QMC::DefaultPropertyFlags, 1),
        // property 'cashSales'
        QtMocHelpers::PropertyData<int>(19, QMetaType::Int, QMC::DefaultPropertyFlags, 1),
        // property 'cardSales'
        QtMocHelpers::PropertyData<int>(20, QMetaType::Int, QMC::DefaultPropertyFlags, 1),
        // property 'orders'
        QtMocHelpers::PropertyData<QVariantList>(21, 0x80000000 | 13, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 1),
    };
    QtMocHelpers::UintData qt_enums {
    };
    QtMocHelpers::UintData qt_constructors {};
    QtMocHelpers::ClassInfos qt_classinfo({
            {    1,    2 },
    });
    return QtMocHelpers::metaObjectData<ReportService, void>(QMC::MetaObjectFlag{}, qt_stringData,
            qt_methods, qt_properties, qt_enums, qt_constructors, qt_classinfo);
}
Q_CONSTINIT const QMetaObject tosspos::ReportService::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN7tosspos13ReportServiceE_t>.stringdata,
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN7tosspos13ReportServiceE_t>.data,
    qt_static_metacall,
    nullptr,
    qt_staticMetaObjectRelocatingContent<qt_meta_tag_ZN7tosspos13ReportServiceE_t>.metaTypes,
    nullptr
} };

void tosspos::ReportService::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    auto *_t = static_cast<ReportService *>(_o);
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: _t->currentDateChanged(); break;
        case 1: _t->reportChanged(); break;
        case 2: _t->refresh(); break;
        case 3: _t->goToToday(); break;
        case 4: _t->previousDay(); break;
        case 5: _t->nextDay(); break;
        case 6: { QString _r = _t->formatDate((*reinterpret_cast< std::add_pointer_t<QDate>>(_a[1])));
            if (_a[0]) *reinterpret_cast< QString*>(_a[0]) = std::move(_r); }  break;
        case 7: { QVariantList _r = _t->getMonthlyReport((*reinterpret_cast< std::add_pointer_t<int>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<int>>(_a[2])));
            if (_a[0]) *reinterpret_cast< QVariantList*>(_a[0]) = std::move(_r); }  break;
        default: ;
        }
    }
    if (_c == QMetaObject::IndexOfMethod) {
        if (QtMocHelpers::indexOfMethod<void (ReportService::*)()>(_a, &ReportService::currentDateChanged, 0))
            return;
        if (QtMocHelpers::indexOfMethod<void (ReportService::*)()>(_a, &ReportService::reportChanged, 1))
            return;
    }
    if (_c == QMetaObject::ReadProperty) {
        void *_v = _a[0];
        switch (_id) {
        case 0: *reinterpret_cast<QDate*>(_v) = _t->currentDate(); break;
        case 1: *reinterpret_cast<int*>(_v) = _t->totalSales(); break;
        case 2: *reinterpret_cast<int*>(_v) = _t->orderCount(); break;
        case 3: *reinterpret_cast<int*>(_v) = _t->cashSales(); break;
        case 4: *reinterpret_cast<int*>(_v) = _t->cardSales(); break;
        case 5: *reinterpret_cast<QVariantList*>(_v) = _t->orders(); break;
        default: break;
        }
    }
    if (_c == QMetaObject::WriteProperty) {
        void *_v = _a[0];
        switch (_id) {
        case 0: _t->setCurrentDate(*reinterpret_cast<QDate*>(_v)); break;
        default: break;
        }
    }
}

const QMetaObject *tosspos::ReportService::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *tosspos::ReportService::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_staticMetaObjectStaticContent<qt_meta_tag_ZN7tosspos13ReportServiceE_t>.strings))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int tosspos::ReportService::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 8)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 8;
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 8)
            *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType();
        _id -= 8;
    }
    if (_c == QMetaObject::ReadProperty || _c == QMetaObject::WriteProperty
            || _c == QMetaObject::ResetProperty || _c == QMetaObject::BindableProperty
            || _c == QMetaObject::RegisterPropertyMetaType) {
        qt_static_metacall(this, _c, _id, _a);
        _id -= 6;
    }
    return _id;
}

// SIGNAL 0
void tosspos::ReportService::currentDateChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void tosspos::ReportService::reportChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}
QT_WARNING_POP
