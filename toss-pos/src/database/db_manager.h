#pragma once

#include <QObject>
#include <QSqlDatabase>
#include <QList>
#include <QDate>
#include "../types/product.h"
#include "../types/order.h"

namespace tosspos {

class DatabaseManager : public QObject
{
    Q_OBJECT

public:
    static DatabaseManager& instance();

    [[nodiscard]] bool initialize(const QString& dbPath = QString());

    // Category operations
    [[nodiscard]] QList<Category> getAllCategories() const;
    [[nodiscard]] bool addCategory(const Category& category);
    [[nodiscard]] bool updateCategory(const Category& category);
    [[nodiscard]] bool deleteCategory(int id);

    // Product operations
    [[nodiscard]] QList<Product> getAllProducts() const;
    [[nodiscard]] QList<Product> getProductsByCategory(int categoryId) const;
    [[nodiscard]] Product getProductById(int id) const;
    [[nodiscard]] bool addProduct(const Product& product);
    [[nodiscard]] bool updateProduct(const Product& product);
    [[nodiscard]] bool deleteProduct(int id);

    // Order operations
    [[nodiscard]] bool saveOrder(const Order& order);
    [[nodiscard]] QList<Order> getOrdersByDate(const QDate& date) const;
    [[nodiscard]] Order getOrderById(int id) const;
    [[nodiscard]] QString generateOrderNo() const;

    // Report operations
    [[nodiscard]] DailyReport getDailyReport(const QDate& date) const;
    [[nodiscard]] QList<DailyReport> getMonthlyReport(int year, int month) const;

private:
    DatabaseManager();
    ~DatabaseManager() override;

    DatabaseManager(const DatabaseManager&) = delete;
    DatabaseManager& operator=(const DatabaseManager&) = delete;

    [[nodiscard]] bool createTables();
    [[nodiscard]] bool insertSampleData();
    [[nodiscard]] bool hasSampleData() const;

    QSqlDatabase m_database;
    QString m_dbPath;
};

} // namespace tosspos
