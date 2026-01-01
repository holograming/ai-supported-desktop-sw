#pragma once

#include <QObject>
#include <QtQml/qqmlregistration.h>
#include "../types/order.h"

namespace tosspos {

class OrderModel;

class OrderService : public QObject
{
    Q_OBJECT
    // Note: Registered as singleton via qmlRegisterSingletonInstance() in main.cpp

public:
    // orderModel: non-owning pointer, caller retains ownership
    explicit OrderService(OrderModel* orderModel, QObject* parent = nullptr);
    ~OrderService() override = default;

    Q_INVOKABLE bool processPayment(const QString& paymentType);
    Q_INVOKABLE QString getLastOrderNo() const { return m_lastOrderNo; }
    Q_INVOKABLE int getLastOrderTotal() const { return m_lastOrderTotal; }

signals:
    void paymentCompleted(const QString& orderNo, int total, const QString& paymentType);
    void paymentFailed(const QString& message);

private:
    OrderModel* m_orderModel;  // Non-owning, caller retains ownership
    QString m_lastOrderNo;
    int m_lastOrderTotal{0};
};

} // namespace tosspos
