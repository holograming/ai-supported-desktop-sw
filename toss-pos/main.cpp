#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQuickStyle>

#include "src/database/db_manager.h"
#include "src/models/category_model.h"
#include "src/models/product_model.h"
#include "src/models/order_model.h"
#include "src/services/order_service.h"
#include "src/services/report_service.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    // 앱 정보 설정
    app.setApplicationName(QStringLiteral("TossPlace POS"));
    app.setApplicationVersion(QStringLiteral("1.0.0"));
    app.setOrganizationName(QStringLiteral("TossPlace"));
    app.setOrganizationDomain(QStringLiteral("tossplace.com"));

    // Material 스타일 설정
    QQuickStyle::setStyle(QStringLiteral("Material"));

    // 데이터베이스 초기화
    tosspos::DatabaseManager& dbManager = tosspos::DatabaseManager::instance();
    if (!dbManager.initialize()) {
        qCritical() << "Failed to initialize database";
        return -1;
    }

    // QML 엔진 생성
    QQmlApplicationEngine engine;

    // 모델 및 서비스 생성 (engine이 parent로 수명 관리)
    auto* categoryModel = new tosspos::CategoryModel(&engine);
    auto* productModel = new tosspos::ProductModel(&engine);
    auto* orderModel = new tosspos::OrderModel(&engine);
    auto* orderService = new tosspos::OrderService(orderModel, &engine);
    auto* reportService = new tosspos::ReportService(&engine);

    // Qt6 권장 방식: qmlRegisterSingletonInstance
    qmlRegisterSingletonInstance("TossPos", 1, 0, "CategoryModel", categoryModel);
    qmlRegisterSingletonInstance("TossPos", 1, 0, "ProductModel", productModel);
    qmlRegisterSingletonInstance("TossPos", 1, 0, "OrderModel", orderModel);
    qmlRegisterSingletonInstance("TossPos", 1, 0, "OrderService", orderService);
    qmlRegisterSingletonInstance("TossPos", 1, 0, "ReportService", reportService);

    // QML 로드
    const QUrl url(QStringLiteral("qrc:/qml/Main.qml"));
    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreationFailed,
        &app,
        []() { QCoreApplication::exit(-1); },
        Qt::QueuedConnection);
    engine.load(url);

    return app.exec();
}
