#pragma once

#include <QAbstractListModel>
#include <QtQml/qqmlregistration.h>
#include "../types/product.h"

namespace tosspos {

class ProductModel : public QAbstractListModel
{
    Q_OBJECT
    QML_ELEMENT

    Q_PROPERTY(int categoryId READ categoryId WRITE setCategoryId NOTIFY categoryIdChanged)
    Q_PROPERTY(int count READ count NOTIFY countChanged)

public:
    enum Roles {
        IdRole = Qt::UserRole + 1,
        CategoryIdRole,
        NameRole,
        PriceRole,
        ImageUrlRole,
        IsActiveRole,
        SortOrderRole
    };

    explicit ProductModel(QObject* parent = nullptr);
    ~ProductModel() override = default;

    // QAbstractListModel interface
    [[nodiscard]] int rowCount(const QModelIndex& parent = QModelIndex()) const override;
    [[nodiscard]] QVariant data(const QModelIndex& index, int role = Qt::DisplayRole) const override;
    [[nodiscard]] QHash<int, QByteArray> roleNames() const override;

    [[nodiscard]] int categoryId() const { return m_categoryId; }
    void setCategoryId(int categoryId);

    [[nodiscard]] int count() const { return static_cast<int>(m_products.size()); }

    Q_INVOKABLE void refresh();
    Q_INVOKABLE QVariantMap getProduct(int index) const;
    Q_INVOKABLE QVariantMap getProductById(int productId) const;

signals:
    void categoryIdChanged();
    void countChanged();

private:
    void loadProducts();

    QList<Product> m_products;
    int m_categoryId{-1};  // -1 means all categories
};

} // namespace tosspos
