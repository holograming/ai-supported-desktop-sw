#pragma once

#include <QObject>
#include <QDate>
#include <QVariantList>
#include <QVariantMap>
#include <QtQml/qqmlregistration.h>

namespace tosspos {

class ReportService : public QObject
{
    Q_OBJECT
    // Note: Registered as singleton via qmlRegisterSingletonInstance() in main.cpp

    Q_PROPERTY(QDate currentDate READ currentDate WRITE setCurrentDate NOTIFY currentDateChanged)
    Q_PROPERTY(int totalSales READ totalSales NOTIFY reportChanged)
    Q_PROPERTY(int orderCount READ orderCount NOTIFY reportChanged)
    Q_PROPERTY(int cashSales READ cashSales NOTIFY reportChanged)
    Q_PROPERTY(int cardSales READ cardSales NOTIFY reportChanged)
    Q_PROPERTY(QVariantList orders READ orders NOTIFY reportChanged)

public:
    explicit ReportService(QObject* parent = nullptr);
    ~ReportService() override = default;

    [[nodiscard]] QDate currentDate() const { return m_currentDate; }
    void setCurrentDate(const QDate& date);

    [[nodiscard]] int totalSales() const { return m_totalSales; }
    [[nodiscard]] int orderCount() const { return m_orderCount; }
    [[nodiscard]] int cashSales() const { return m_cashSales; }
    [[nodiscard]] int cardSales() const { return m_cardSales; }
    [[nodiscard]] QVariantList orders() const { return m_orders; }

    Q_INVOKABLE void refresh();
    Q_INVOKABLE void goToToday();
    Q_INVOKABLE void previousDay();
    Q_INVOKABLE void nextDay();
    Q_INVOKABLE QString formatDate(const QDate& date) const;
    Q_INVOKABLE QVariantList getMonthlyReport(int year, int month) const;

signals:
    void currentDateChanged();
    void reportChanged();

private:
    void loadReport();

    QDate m_currentDate;
    int m_totalSales{0};
    int m_orderCount{0};
    int m_cashSales{0};
    int m_cardSales{0};
    QVariantList m_orders;
};

} // namespace tosspos
