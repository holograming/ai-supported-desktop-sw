#include "order_service.h"
#include "../models/order_model.h"
#include "../database/db_manager.h"

#include <QDateTime>
#include <QDebug>

namespace tosspos {

OrderService::OrderService(OrderModel* orderModel, QObject* parent)
    : QObject(parent)
    , m_orderModel(orderModel)
{
}

bool OrderService::processPayment(const QString& paymentType)
{
    if (!m_orderModel || m_orderModel->isEmpty()) {
        emit paymentFailed(QStringLiteral("주문 목록이 비어있습니다."));
        return false;
    }

    // 유효한 결제 타입 확인
    if (paymentType != QStringLiteral("CASH") && paymentType != QStringLiteral("CARD")) {
        emit paymentFailed(QStringLiteral("잘못된 결제 타입입니다."));
        return false;
    }

    // 주문 생성
    Order order;
    order.orderNo = DatabaseManager::instance().generateOrderNo();
    order.total = m_orderModel->totalAmount();
    order.paymentType = paymentType;
    order.status = QStringLiteral("COMPLETED");
    order.createdAt = QDateTime::currentDateTime();
    order.completedAt = QDateTime::currentDateTime();
    order.items = m_orderModel->getItems();

    // 데이터베이스에 저장
    if (!DatabaseManager::instance().saveOrder(order)) {
        emit paymentFailed(QStringLiteral("주문 저장에 실패했습니다."));
        return false;
    }

    // 마지막 주문 정보 저장
    m_lastOrderNo = order.orderNo;
    m_lastOrderTotal = order.total;

    // 주문 목록 초기화
    m_orderModel->clear();

    // 성공 시그널 발생
    emit paymentCompleted(order.orderNo, order.total, paymentType);

    qDebug() << "Payment completed:" << order.orderNo
             << "Total:" << order.total
             << "Type:" << paymentType;

    return true;
}

} // namespace tosspos
