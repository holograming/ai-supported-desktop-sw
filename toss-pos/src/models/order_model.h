#pragma once

#include <QAbstractListModel>
#include <QtQml/qqmlregistration.h>
#include "../types/order.h"

namespace tosspos {

class OrderModel : public QAbstractListModel
{
    Q_OBJECT
    // Note: Registered as singleton via qmlRegisterSingletonInstance() in main.cpp

    Q_PROPERTY(int count READ count NOTIFY countChanged)
    Q_PROPERTY(int totalAmount READ totalAmount NOTIFY totalAmountChanged)
    Q_PROPERTY(bool isEmpty READ isEmpty NOTIFY countChanged)

public:
    enum Roles {
        ProductIdRole = Qt::UserRole + 1,
        ProductNameRole,
        QuantityRole,
        UnitPriceRole,
        SubtotalRole
    };

    explicit OrderModel(QObject* parent = nullptr);
    ~OrderModel() override = default;

    // QAbstractListModel interface
    [[nodiscard]] int rowCount(const QModelIndex& parent = QModelIndex()) const override;
    [[nodiscard]] QVariant data(const QModelIndex& index, int role = Qt::DisplayRole) const override;
    [[nodiscard]] QHash<int, QByteArray> roleNames() const override;

    [[nodiscard]] int count() const { return static_cast<int>(m_items.size()); }
    [[nodiscard]] int totalAmount() const { return m_totalAmount; }
    [[nodiscard]] bool isEmpty() const { return m_items.isEmpty(); }

    // Cart operations
    Q_INVOKABLE void addItem(int productId, const QString& productName, int price);
    Q_INVOKABLE void removeItem(int index);
    Q_INVOKABLE void increaseQuantity(int index);
    Q_INVOKABLE void decreaseQuantity(int index);
    Q_INVOKABLE void clear();

    // Get current items for order processing
    [[nodiscard]] QList<OrderItem> getItems() const { return m_items; }

signals:
    void countChanged();
    void totalAmountChanged();

private:
    void recalculateTotal();

    QList<OrderItem> m_items;
    int m_totalAmount{0};
};

} // namespace tosspos
