#include "report_service.h"
#include "../database/db_manager.h"

#include <QLocale>

namespace tosspos {

ReportService::ReportService(QObject* parent)
    : QObject(parent)
    , m_currentDate(QDate::currentDate())
{
    loadReport();
}

void ReportService::setCurrentDate(const QDate& date)
{
    if (m_currentDate != date) {
        m_currentDate = date;
        emit currentDateChanged();
        loadReport();
    }
}

void ReportService::refresh()
{
    loadReport();
}

void ReportService::goToToday()
{
    setCurrentDate(QDate::currentDate());
}

void ReportService::previousDay()
{
    setCurrentDate(m_currentDate.addDays(-1));
}

void ReportService::nextDay()
{
    setCurrentDate(m_currentDate.addDays(1));
}

QString ReportService::formatDate(const QDate& date) const
{
    const QLocale locale(QLocale::Korean);
    return locale.toString(date, QStringLiteral("yyyy년 M월 d일 (ddd)"));
}

void ReportService::loadReport()
{
    // 일별 리포트 조회
    const auto report = DatabaseManager::instance().getDailyReport(m_currentDate);
    m_totalSales = report.totalSales;
    m_orderCount = report.orderCount;
    m_cashSales = report.cashSales;
    m_cardSales = report.cardSales;

    // 주문 내역 조회
    m_orders.clear();
    const auto orders = DatabaseManager::instance().getOrdersByDate(m_currentDate);
    for (const auto& order : orders) {
        QVariantMap orderMap;
        orderMap[QStringLiteral("id")] = order.id;
        orderMap[QStringLiteral("orderNo")] = order.orderNo;
        orderMap[QStringLiteral("total")] = order.total;
        orderMap[QStringLiteral("paymentType")] = order.paymentType;
        orderMap[QStringLiteral("status")] = order.status;
        orderMap[QStringLiteral("createdAt")] = order.createdAt.toString(QStringLiteral("HH:mm"));

        // 주문 항목
        QVariantList itemList;
        for (const auto& item : order.items) {
            QVariantMap itemMap;
            itemMap[QStringLiteral("productName")] = item.productName;
            itemMap[QStringLiteral("quantity")] = item.quantity;
            itemMap[QStringLiteral("unitPrice")] = item.unitPrice;
            itemMap[QStringLiteral("subtotal")] = item.subtotal;
            itemList.append(itemMap);
        }
        orderMap[QStringLiteral("items")] = itemList;

        m_orders.append(orderMap);
    }

    emit reportChanged();
}

QVariantList ReportService::getMonthlyReport(int year, int month) const
{
    QVariantList result;
    const auto reports = DatabaseManager::instance().getMonthlyReport(year, month);

    for (const auto& report : reports) {
        QVariantMap map;
        map[QStringLiteral("date")] = report.date;
        map[QStringLiteral("totalSales")] = report.totalSales;
        map[QStringLiteral("orderCount")] = report.orderCount;
        map[QStringLiteral("cashSales")] = report.cashSales;
        map[QStringLiteral("cardSales")] = report.cardSales;
        result.append(map);
    }

    return result;
}

} // namespace tosspos
