/****************************************************************************
** Generated QML type registration code
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <QtQml/qqml.h>
#include <QtQml/qqmlmoduleregistration.h>

#if __has_include(<category_model.h>)
#  include <category_model.h>
#endif
#if __has_include(<order_model.h>)
#  include <order_model.h>
#endif
#if __has_include(<order_service.h>)
#  include <order_service.h>
#endif
#if __has_include(<product_model.h>)
#  include <product_model.h>
#endif
#if __has_include(<report_service.h>)
#  include <report_service.h>
#endif


#if !defined(QT_STATIC)
#define Q_QMLTYPE_EXPORT Q_DECL_EXPORT
#else
#define Q_QMLTYPE_EXPORT
#endif
Q_QMLTYPE_EXPORT void qml_register_types_TossPos()
{
    QT_WARNING_PUSH QT_WARNING_DISABLE_DEPRECATED
    qmlRegisterTypesAndRevisions<tosspos::CategoryModel>("TossPos", 1);
    qmlRegisterAnonymousType<QAbstractItemModel, 254>("TossPos", 1);
    qmlRegisterTypesAndRevisions<tosspos::OrderModel>("TossPos", 1);
    qmlRegisterTypesAndRevisions<tosspos::OrderService>("TossPos", 1);
    qmlRegisterTypesAndRevisions<tosspos::ProductModel>("TossPos", 1);
    qmlRegisterTypesAndRevisions<tosspos::ReportService>("TossPos", 1);
    QT_WARNING_POP
    qmlRegisterModule("TossPos", 1, 0);
}

static const QQmlModuleRegistration tossPosRegistration("TossPos", qml_register_types_TossPos);
