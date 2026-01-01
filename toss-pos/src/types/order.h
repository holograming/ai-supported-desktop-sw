#pragma once

#include <QString>
#include <QDateTime>
#include <QList>

namespace tosspos {

struct OrderItem
{
    int id{0};
    int orderId{0};
    int productId{0};
    QString productName;
    int quantity{0};
    int unitPrice{0};
    int subtotal{0};
};

struct Order
{
    int id{0};
    QString orderNo;
    int total{0};
    QString paymentType;  // "CASH" or "CARD"
    QString status;       // "COMPLETED", "CANCELLED"
    QDateTime createdAt;
    QDateTime completedAt;
    QList<OrderItem> items;
};

struct DailyReport
{
    QDate date;
    int totalSales{0};
    int orderCount{0};
    int cashSales{0};
    int cardSales{0};
};

} // namespace tosspos
