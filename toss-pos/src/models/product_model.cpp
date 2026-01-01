#include "product_model.h"
#include "../database/db_manager.h"

namespace tosspos {

ProductModel::ProductModel(QObject* parent)
    : QAbstractListModel(parent)
{
    loadProducts();
}

int ProductModel::rowCount(const QModelIndex& parent) const
{
    if (parent.isValid()) {
        return 0;
    }
    return static_cast<int>(m_products.size());
}

QVariant ProductModel::data(const QModelIndex& index, int role) const
{
    if (!index.isValid() || index.row() < 0 || index.row() >= m_products.size()) {
        return QVariant();
    }

    const Product& product = m_products.at(index.row());

    switch (role) {
    case IdRole:
        return product.id;
    case CategoryIdRole:
        return product.categoryId;
    case NameRole:
        return product.name;
    case PriceRole:
        return product.price;
    case ImageUrlRole:
        return product.imageUrl;
    case IsActiveRole:
        return product.isActive;
    case SortOrderRole:
        return product.sortOrder;
    default:
        return QVariant();
    }
}

QHash<int, QByteArray> ProductModel::roleNames() const
{
    return {
        {IdRole, "productId"},
        {CategoryIdRole, "categoryId"},
        {NameRole, "name"},
        {PriceRole, "price"},
        {ImageUrlRole, "imageUrl"},
        {IsActiveRole, "isActive"},
        {SortOrderRole, "sortOrder"}
    };
}

void ProductModel::setCategoryId(int categoryId)
{
    if (m_categoryId != categoryId) {
        m_categoryId = categoryId;
        emit categoryIdChanged();
        loadProducts();
    }
}

void ProductModel::refresh()
{
    loadProducts();
}

void ProductModel::loadProducts()
{
    beginResetModel();
    if (m_categoryId <= 0) {
        m_products = DatabaseManager::instance().getAllProducts();
    } else {
        m_products = DatabaseManager::instance().getProductsByCategory(m_categoryId);
    }
    endResetModel();
    emit countChanged();
}

QVariantMap ProductModel::getProduct(int index) const
{
    QVariantMap result;
    if (index < 0 || index >= m_products.size()) {
        return result;
    }

    const Product& product = m_products.at(index);
    result[QStringLiteral("productId")] = product.id;
    result[QStringLiteral("categoryId")] = product.categoryId;
    result[QStringLiteral("name")] = product.name;
    result[QStringLiteral("price")] = product.price;
    result[QStringLiteral("imageUrl")] = product.imageUrl;
    result[QStringLiteral("isActive")] = product.isActive;

    return result;
}

QVariantMap ProductModel::getProductById(int productId) const
{
    QVariantMap result;
    for (const auto& product : m_products) {
        if (product.id == productId) {
            result[QStringLiteral("productId")] = product.id;
            result[QStringLiteral("categoryId")] = product.categoryId;
            result[QStringLiteral("name")] = product.name;
            result[QStringLiteral("price")] = product.price;
            result[QStringLiteral("imageUrl")] = product.imageUrl;
            result[QStringLiteral("isActive")] = product.isActive;
            break;
        }
    }
    return result;
}

} // namespace tosspos
