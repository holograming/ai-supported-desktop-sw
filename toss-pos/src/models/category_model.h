#pragma once

#include <QAbstractListModel>
#include <QtQml/qqmlregistration.h>
#include "../types/product.h"

namespace tosspos {

class CategoryModel : public QAbstractListModel
{
    Q_OBJECT
    // Note: Registered as singleton via qmlRegisterSingletonInstance() in main.cpp

    Q_PROPERTY(int count READ count NOTIFY countChanged)

public:
    enum Roles {
        IdRole = Qt::UserRole + 1,
        NameRole,
        IconRole,
        SortOrderRole
    };

    explicit CategoryModel(QObject* parent = nullptr);
    ~CategoryModel() override = default;

    // QAbstractListModel interface
    [[nodiscard]] int rowCount(const QModelIndex& parent = QModelIndex()) const override;
    [[nodiscard]] QVariant data(const QModelIndex& index, int role = Qt::DisplayRole) const override;
    [[nodiscard]] QHash<int, QByteArray> roleNames() const override;

    [[nodiscard]] int count() const { return static_cast<int>(m_categories.size()); }

    Q_INVOKABLE void refresh();
    Q_INVOKABLE int getCategoryId(int index) const;
    Q_INVOKABLE QString getCategoryName(int index) const;

signals:
    void countChanged();

private:
    QList<Category> m_categories;
};

} // namespace tosspos
