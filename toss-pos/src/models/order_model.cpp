#include "order_model.h"

namespace tosspos {

OrderModel::OrderModel(QObject* parent)
    : QAbstractListModel(parent)
{
}

int OrderModel::rowCount(const QModelIndex& parent) const
{
    if (parent.isValid()) {
        return 0;
    }
    return static_cast<int>(m_items.size());
}

QVariant OrderModel::data(const QModelIndex& index, int role) const
{
    if (!index.isValid() || index.row() < 0 || index.row() >= m_items.size()) {
        return QVariant();
    }

    const OrderItem& item = m_items.at(index.row());

    switch (role) {
    case ProductIdRole:
        return item.productId;
    case ProductNameRole:
        return item.productName;
    case QuantityRole:
        return item.quantity;
    case UnitPriceRole:
        return item.unitPrice;
    case SubtotalRole:
        return item.subtotal;
    default:
        return QVariant();
    }
}

QHash<int, QByteArray> OrderModel::roleNames() const
{
    return {
        {ProductIdRole, "productId"},
        {ProductNameRole, "productName"},
        {QuantityRole, "quantity"},
        {UnitPriceRole, "unitPrice"},
        {SubtotalRole, "subtotal"}
    };
}

void OrderModel::addItem(int productId, const QString& productName, int price)
{
    // 이미 존재하는 상품인지 확인
    for (int i = 0; i < m_items.size(); ++i) {
        if (m_items[i].productId == productId) {
            // 수량 증가
            m_items[i].quantity++;
            m_items[i].subtotal = m_items[i].quantity * m_items[i].unitPrice;

            QModelIndex idx = index(i);
            emit dataChanged(idx, idx, {QuantityRole, SubtotalRole});
            recalculateTotal();
            return;
        }
    }

    // 새 항목 추가
    OrderItem item;
    item.productId = productId;
    item.productName = productName;
    item.quantity = 1;
    item.unitPrice = price;
    item.subtotal = price;

    beginInsertRows(QModelIndex(), m_items.size(), m_items.size());
    m_items.append(item);
    endInsertRows();

    emit countChanged();
    recalculateTotal();
}

void OrderModel::removeItem(int index)
{
    if (index < 0 || index >= m_items.size()) {
        return;
    }

    beginRemoveRows(QModelIndex(), index, index);
    m_items.removeAt(index);
    endRemoveRows();

    emit countChanged();
    recalculateTotal();
}

void OrderModel::increaseQuantity(int index)
{
    if (index < 0 || index >= m_items.size()) {
        return;
    }

    m_items[index].quantity++;
    m_items[index].subtotal = m_items[index].quantity * m_items[index].unitPrice;

    QModelIndex idx = this->index(index);
    emit dataChanged(idx, idx, {QuantityRole, SubtotalRole});
    recalculateTotal();
}

void OrderModel::decreaseQuantity(int index)
{
    if (index < 0 || index >= m_items.size()) {
        return;
    }

    if (m_items[index].quantity <= 1) {
        // 수량이 1이면 항목 삭제
        removeItem(index);
    } else {
        m_items[index].quantity--;
        m_items[index].subtotal = m_items[index].quantity * m_items[index].unitPrice;

        QModelIndex idx = this->index(index);
        emit dataChanged(idx, idx, {QuantityRole, SubtotalRole});
        recalculateTotal();
    }
}

void OrderModel::clear()
{
    if (m_items.isEmpty()) {
        return;
    }

    beginResetModel();
    m_items.clear();
    endResetModel();

    emit countChanged();
    recalculateTotal();
}

void OrderModel::recalculateTotal()
{
    int total = 0;
    for (const auto& item : m_items) {
        total += item.subtotal;
    }

    if (m_totalAmount != total) {
        m_totalAmount = total;
        emit totalAmountChanged();
    }
}

} // namespace tosspos
