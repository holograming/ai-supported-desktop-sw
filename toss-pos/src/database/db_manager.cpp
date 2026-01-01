#include "db_manager.h"

#include <QSqlQuery>
#include <QSqlError>
#include <QStandardPaths>
#include <QDir>
#include <QDateTime>
#include <QDebug>

namespace tosspos {

DatabaseManager& DatabaseManager::instance()
{
    static DatabaseManager instance;
    return instance;
}

DatabaseManager::DatabaseManager()
    : QObject(nullptr)
{
}

DatabaseManager::~DatabaseManager()
{
    if (m_database.isOpen()) {
        m_database.close();
    }
}

bool DatabaseManager::initialize(const QString& dbPath)
{
    // 데이터베이스 경로 설정
    if (dbPath.isEmpty()) {
        const QString dataPath = QStandardPaths::writableLocation(QStandardPaths::AppDataLocation);
        QDir dir(dataPath);
        if (!dir.exists()) {
            dir.mkpath(dataPath);
        }
        m_dbPath = dataPath + QStringLiteral("/tosspos.db");
    } else {
        m_dbPath = dbPath;
    }

    qDebug() << "Database path:" << m_dbPath;

    // SQLite 연결
    m_database = QSqlDatabase::addDatabase(QStringLiteral("QSQLITE"));
    m_database.setDatabaseName(m_dbPath);

    if (!m_database.open()) {
        qCritical() << "Failed to open database:" << m_database.lastError().text();
        return false;
    }

    // 외래키 활성화
    QSqlQuery query(m_database);
    query.exec(QStringLiteral("PRAGMA foreign_keys = ON"));

    // 테이블 생성
    if (!createTables()) {
        qCritical() << "Failed to create tables";
        return false;
    }

    // 샘플 데이터 삽입
    if (!hasSampleData()) {
        if (!insertSampleData()) {
            qWarning() << "Failed to insert sample data";
        }
    }

    qDebug() << "Database initialized successfully";
    return true;
}

bool DatabaseManager::createTables()
{
    QSqlQuery query(m_database);

    // 카테고리 테이블
    const QString createCategories = QStringLiteral(R"(
        CREATE TABLE IF NOT EXISTS categories (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            icon        TEXT,
            sort_order  INTEGER DEFAULT 0,
            created_at  TEXT DEFAULT (datetime('now', 'localtime'))
        )
    )");

    if (!query.exec(createCategories)) {
        qCritical() << "Failed to create categories table:" << query.lastError().text();
        return false;
    }

    // 상품 테이블
    const QString createProducts = QStringLiteral(R"(
        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            name        TEXT NOT NULL,
            price       INTEGER NOT NULL,
            image_url   TEXT,
            is_active   INTEGER DEFAULT 1,
            sort_order  INTEGER DEFAULT 0,
            created_at  TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    )");

    if (!query.exec(createProducts)) {
        qCritical() << "Failed to create products table:" << query.lastError().text();
        return false;
    }

    // 주문 테이블
    const QString createOrders = QStringLiteral(R"(
        CREATE TABLE IF NOT EXISTS orders (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no     TEXT NOT NULL UNIQUE,
            total        INTEGER NOT NULL,
            payment_type TEXT NOT NULL,
            status       TEXT DEFAULT 'COMPLETED',
            created_at   TEXT DEFAULT (datetime('now', 'localtime')),
            completed_at TEXT
        )
    )");

    if (!query.exec(createOrders)) {
        qCritical() << "Failed to create orders table:" << query.lastError().text();
        return false;
    }

    // 주문 항목 테이블
    const QString createOrderItems = QStringLiteral(R"(
        CREATE TABLE IF NOT EXISTS order_items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id    INTEGER NOT NULL,
            product_id  INTEGER NOT NULL,
            quantity    INTEGER NOT NULL,
            unit_price  INTEGER NOT NULL,
            subtotal    INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    )");

    if (!query.exec(createOrderItems)) {
        qCritical() << "Failed to create order_items table:" << query.lastError().text();
        return false;
    }

    return true;
}

bool DatabaseManager::hasSampleData() const
{
    QSqlQuery query(m_database);
    query.exec(QStringLiteral("SELECT COUNT(*) FROM categories"));
    if (query.next()) {
        return query.value(0).toInt() > 0;
    }
    return false;
}

bool DatabaseManager::insertSampleData()
{
    QSqlQuery query(m_database);

    // 트랜잭션 시작
    m_database.transaction();

    // 카테고리 삽입
    const QString insertCategories = QStringLiteral(R"(
        INSERT INTO categories (name, icon, sort_order) VALUES
        ('커피', 'coffee', 1),
        ('음료', 'cup', 2),
        ('디저트', 'cake', 3),
        ('베이커리', 'bread', 4)
    )");

    if (!query.exec(insertCategories)) {
        qCritical() << "Failed to insert categories:" << query.lastError().text();
        m_database.rollback();
        return false;
    }

    // 상품 삽입
    const QString insertProducts = QStringLiteral(R"(
        INSERT INTO products (category_id, name, price, sort_order) VALUES
        (1, '아메리카노', 4500, 1),
        (1, '카페라떼', 5000, 2),
        (1, '바닐라라떼', 5500, 3),
        (1, '카푸치노', 5000, 4),
        (1, '에스프레소', 3500, 5),
        (1, '카라멜마끼아또', 5500, 6),
        (1, '콜드브루', 5000, 7),
        (2, '자몽에이드', 5500, 1),
        (2, '레몬에이드', 5000, 2),
        (2, '아이스티', 4500, 3),
        (2, '밀크티', 5500, 4),
        (2, '초코라떼', 5000, 5),
        (3, '치즈케이크', 6500, 1),
        (3, '티라미수', 7000, 2),
        (3, '마카롱 세트', 8000, 3),
        (3, '브라우니', 5500, 4),
        (4, '크로와상', 4000, 1),
        (4, '베이글', 3500, 2),
        (4, '머핀', 4500, 3),
        (4, '스콘', 4000, 4)
    )");

    if (!query.exec(insertProducts)) {
        qCritical() << "Failed to insert products:" << query.lastError().text();
        m_database.rollback();
        return false;
    }

    m_database.commit();
    qDebug() << "Sample data inserted successfully";
    return true;
}

// Category operations
QList<Category> DatabaseManager::getAllCategories() const
{
    QList<Category> categories;
    QSqlQuery query(m_database);
    query.exec(QStringLiteral("SELECT id, name, icon, sort_order FROM categories ORDER BY sort_order"));

    while (query.next()) {
        Category cat;
        cat.id = query.value(0).toInt();
        cat.name = query.value(1).toString();
        cat.icon = query.value(2).toString();
        cat.sortOrder = query.value(3).toInt();
        categories.append(cat);
    }

    return categories;
}

bool DatabaseManager::addCategory(const Category& category)
{
    QSqlQuery query(m_database);
    query.prepare(QStringLiteral("INSERT INTO categories (name, icon, sort_order) VALUES (?, ?, ?)"));
    query.addBindValue(category.name);
    query.addBindValue(category.icon);
    query.addBindValue(category.sortOrder);
    return query.exec();
}

bool DatabaseManager::updateCategory(const Category& category)
{
    QSqlQuery query(m_database);
    query.prepare(QStringLiteral("UPDATE categories SET name = ?, icon = ?, sort_order = ? WHERE id = ?"));
    query.addBindValue(category.name);
    query.addBindValue(category.icon);
    query.addBindValue(category.sortOrder);
    query.addBindValue(category.id);
    return query.exec();
}

bool DatabaseManager::deleteCategory(int id)
{
    // 해당 카테고리에 상품이 있는지 확인
    QSqlQuery checkQuery(m_database);
    checkQuery.prepare(QStringLiteral("SELECT COUNT(*) FROM products WHERE category_id = ?"));
    checkQuery.addBindValue(id);
    checkQuery.exec();
    if (checkQuery.next() && checkQuery.value(0).toInt() > 0) {
        return false;  // 상품이 있으면 삭제 불가
    }

    QSqlQuery query(m_database);
    query.prepare(QStringLiteral("DELETE FROM categories WHERE id = ?"));
    query.addBindValue(id);
    return query.exec();
}

// Product operations
QList<Product> DatabaseManager::getAllProducts() const
{
    QList<Product> products;
    QSqlQuery query(m_database);
    query.exec(QStringLiteral(
        "SELECT id, category_id, name, price, image_url, is_active, sort_order "
        "FROM products WHERE is_active = 1 ORDER BY category_id, sort_order"
    ));

    while (query.next()) {
        Product prod;
        prod.id = query.value(0).toInt();
        prod.categoryId = query.value(1).toInt();
        prod.name = query.value(2).toString();
        prod.price = query.value(3).toInt();
        prod.imageUrl = query.value(4).toString();
        prod.isActive = query.value(5).toBool();
        prod.sortOrder = query.value(6).toInt();
        products.append(prod);
    }

    return products;
}

QList<Product> DatabaseManager::getProductsByCategory(int categoryId) const
{
    QList<Product> products;
    QSqlQuery query(m_database);
    query.prepare(QStringLiteral(
        "SELECT id, category_id, name, price, image_url, is_active, sort_order "
        "FROM products WHERE category_id = ? AND is_active = 1 ORDER BY sort_order"
    ));
    query.addBindValue(categoryId);
    query.exec();

    while (query.next()) {
        Product prod;
        prod.id = query.value(0).toInt();
        prod.categoryId = query.value(1).toInt();
        prod.name = query.value(2).toString();
        prod.price = query.value(3).toInt();
        prod.imageUrl = query.value(4).toString();
        prod.isActive = query.value(5).toBool();
        prod.sortOrder = query.value(6).toInt();
        products.append(prod);
    }

    return products;
}

Product DatabaseManager::getProductById(int id) const
{
    Product prod;
    QSqlQuery query(m_database);
    query.prepare(QStringLiteral(
        "SELECT id, category_id, name, price, image_url, is_active, sort_order "
        "FROM products WHERE id = ?"
    ));
    query.addBindValue(id);
    query.exec();

    if (query.next()) {
        prod.id = query.value(0).toInt();
        prod.categoryId = query.value(1).toInt();
        prod.name = query.value(2).toString();
        prod.price = query.value(3).toInt();
        prod.imageUrl = query.value(4).toString();
        prod.isActive = query.value(5).toBool();
        prod.sortOrder = query.value(6).toInt();
    }

    return prod;
}

bool DatabaseManager::addProduct(const Product& product)
{
    QSqlQuery query(m_database);
    query.prepare(QStringLiteral(
        "INSERT INTO products (category_id, name, price, image_url, is_active, sort_order) "
        "VALUES (?, ?, ?, ?, ?, ?)"
    ));
    query.addBindValue(product.categoryId);
    query.addBindValue(product.name);
    query.addBindValue(product.price);
    query.addBindValue(product.imageUrl);
    query.addBindValue(product.isActive ? 1 : 0);
    query.addBindValue(product.sortOrder);
    return query.exec();
}

bool DatabaseManager::updateProduct(const Product& product)
{
    QSqlQuery query(m_database);
    query.prepare(QStringLiteral(
        "UPDATE products SET category_id = ?, name = ?, price = ?, "
        "image_url = ?, is_active = ?, sort_order = ? WHERE id = ?"
    ));
    query.addBindValue(product.categoryId);
    query.addBindValue(product.name);
    query.addBindValue(product.price);
    query.addBindValue(product.imageUrl);
    query.addBindValue(product.isActive ? 1 : 0);
    query.addBindValue(product.sortOrder);
    query.addBindValue(product.id);
    return query.exec();
}

bool DatabaseManager::deleteProduct(int id)
{
    QSqlQuery query(m_database);
    query.prepare(QStringLiteral("UPDATE products SET is_active = 0 WHERE id = ?"));
    query.addBindValue(id);
    return query.exec();
}

// Order operations
QString DatabaseManager::generateOrderNo() const
{
    const QString dateStr = QDate::currentDate().toString(QStringLiteral("yyyyMMdd"));

    QSqlQuery query(m_database);
    query.prepare(QStringLiteral(
        "SELECT COUNT(*) FROM orders WHERE order_no LIKE ?"
    ));
    query.addBindValue(dateStr + QStringLiteral("%"));
    query.exec();

    int seq = 1;
    if (query.next()) {
        seq = query.value(0).toInt() + 1;
    }

    return QStringLiteral("%1-%2").arg(dateStr).arg(seq, 4, 10, QLatin1Char('0'));
}

bool DatabaseManager::saveOrder(const Order& order)
{
    m_database.transaction();

    QSqlQuery query(m_database);

    // 주문 저장
    query.prepare(QStringLiteral(
        "INSERT INTO orders (order_no, total, payment_type, status, created_at, completed_at) "
        "VALUES (?, ?, ?, ?, ?, ?)"
    ));
    query.addBindValue(order.orderNo);
    query.addBindValue(order.total);
    query.addBindValue(order.paymentType);
    query.addBindValue(order.status);
    query.addBindValue(order.createdAt.toString(Qt::ISODate));
    query.addBindValue(order.completedAt.toString(Qt::ISODate));

    if (!query.exec()) {
        qCritical() << "Failed to save order:" << query.lastError().text();
        m_database.rollback();
        return false;
    }

    const int orderId = query.lastInsertId().toInt();

    // 주문 항목 저장
    for (const auto& item : order.items) {
        query.prepare(QStringLiteral(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) "
            "VALUES (?, ?, ?, ?, ?)"
        ));
        query.addBindValue(orderId);
        query.addBindValue(item.productId);
        query.addBindValue(item.quantity);
        query.addBindValue(item.unitPrice);
        query.addBindValue(item.subtotal);

        if (!query.exec()) {
            qCritical() << "Failed to save order item:" << query.lastError().text();
            m_database.rollback();
            return false;
        }
    }

    m_database.commit();
    qDebug() << "Order saved:" << order.orderNo;
    return true;
}

QList<Order> DatabaseManager::getOrdersByDate(const QDate& date) const
{
    QList<Order> orders;
    QSqlQuery query(m_database);

    query.prepare(QStringLiteral(
        "SELECT id, order_no, total, payment_type, status, created_at, completed_at "
        "FROM orders WHERE date(created_at) = ? ORDER BY created_at DESC"
    ));
    query.addBindValue(date.toString(Qt::ISODate));
    query.exec();

    while (query.next()) {
        Order order;
        order.id = query.value(0).toInt();
        order.orderNo = query.value(1).toString();
        order.total = query.value(2).toInt();
        order.paymentType = query.value(3).toString();
        order.status = query.value(4).toString();
        order.createdAt = QDateTime::fromString(query.value(5).toString(), Qt::ISODate);
        order.completedAt = QDateTime::fromString(query.value(6).toString(), Qt::ISODate);

        // 주문 항목 조회
        QSqlQuery itemQuery(m_database);
        itemQuery.prepare(QStringLiteral(
            "SELECT oi.id, oi.product_id, p.name, oi.quantity, oi.unit_price, oi.subtotal "
            "FROM order_items oi "
            "JOIN products p ON oi.product_id = p.id "
            "WHERE oi.order_id = ?"
        ));
        itemQuery.addBindValue(order.id);
        itemQuery.exec();

        while (itemQuery.next()) {
            OrderItem item;
            item.id = itemQuery.value(0).toInt();
            item.orderId = order.id;
            item.productId = itemQuery.value(1).toInt();
            item.productName = itemQuery.value(2).toString();
            item.quantity = itemQuery.value(3).toInt();
            item.unitPrice = itemQuery.value(4).toInt();
            item.subtotal = itemQuery.value(5).toInt();
            order.items.append(item);
        }

        orders.append(order);
    }

    return orders;
}

Order DatabaseManager::getOrderById(int id) const
{
    Order order;
    QSqlQuery query(m_database);

    query.prepare(QStringLiteral(
        "SELECT id, order_no, total, payment_type, status, created_at, completed_at "
        "FROM orders WHERE id = ?"
    ));
    query.addBindValue(id);
    query.exec();

    if (query.next()) {
        order.id = query.value(0).toInt();
        order.orderNo = query.value(1).toString();
        order.total = query.value(2).toInt();
        order.paymentType = query.value(3).toString();
        order.status = query.value(4).toString();
        order.createdAt = QDateTime::fromString(query.value(5).toString(), Qt::ISODate);
        order.completedAt = QDateTime::fromString(query.value(6).toString(), Qt::ISODate);
    }

    return order;
}

// Report operations
DailyReport DatabaseManager::getDailyReport(const QDate& date) const
{
    DailyReport report;
    report.date = date;

    QSqlQuery query(m_database);

    // 총 매출 및 주문 수
    query.prepare(QStringLiteral(
        "SELECT COUNT(*), COALESCE(SUM(total), 0) FROM orders "
        "WHERE date(created_at) = ? AND status = 'COMPLETED'"
    ));
    query.addBindValue(date.toString(Qt::ISODate));
    query.exec();

    if (query.next()) {
        report.orderCount = query.value(0).toInt();
        report.totalSales = query.value(1).toInt();
    }

    // 현금 매출
    query.prepare(QStringLiteral(
        "SELECT COALESCE(SUM(total), 0) FROM orders "
        "WHERE date(created_at) = ? AND status = 'COMPLETED' AND payment_type = 'CASH'"
    ));
    query.addBindValue(date.toString(Qt::ISODate));
    query.exec();

    if (query.next()) {
        report.cashSales = query.value(0).toInt();
    }

    // 카드 매출
    query.prepare(QStringLiteral(
        "SELECT COALESCE(SUM(total), 0) FROM orders "
        "WHERE date(created_at) = ? AND status = 'COMPLETED' AND payment_type = 'CARD'"
    ));
    query.addBindValue(date.toString(Qt::ISODate));
    query.exec();

    if (query.next()) {
        report.cardSales = query.value(0).toInt();
    }

    return report;
}

QList<DailyReport> DatabaseManager::getMonthlyReport(int year, int month) const
{
    QList<DailyReport> reports;

    const QDate startDate(year, month, 1);
    const QDate endDate = startDate.addMonths(1).addDays(-1);

    for (QDate date = startDate; date <= endDate; date = date.addDays(1)) {
        DailyReport report = getDailyReport(date);
        if (report.orderCount > 0) {
            reports.append(report);
        }
    }

    return reports;
}

} // namespace tosspos
