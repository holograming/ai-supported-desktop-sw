#include "category_model.h"
#include "../database/db_manager.h"

namespace tosspos {

CategoryModel::CategoryModel(QObject* parent)
    : QAbstractListModel(parent)
{
    refresh();
}

int CategoryModel::rowCount(const QModelIndex& parent) const
{
    if (parent.isValid()) {
        return 0;
    }
    return static_cast<int>(m_categories.size());
}

QVariant CategoryModel::data(const QModelIndex& index, int role) const
{
    if (!index.isValid() || index.row() < 0 || index.row() >= m_categories.size()) {
        return QVariant();
    }

    const Category& category = m_categories.at(index.row());

    switch (role) {
    case IdRole:
        return category.id;
    case NameRole:
        return category.name;
    case IconRole:
        return category.icon;
    case SortOrderRole:
        return category.sortOrder;
    default:
        return QVariant();
    }
}

QHash<int, QByteArray> CategoryModel::roleNames() const
{
    return {
        {IdRole, "categoryId"},
        {NameRole, "name"},
        {IconRole, "icon"},
        {SortOrderRole, "sortOrder"}
    };
}

void CategoryModel::refresh()
{
    beginResetModel();
    m_categories = DatabaseManager::instance().getAllCategories();
    endResetModel();
    emit countChanged();
}

int CategoryModel::getCategoryId(int index) const
{
    if (index < 0 || index >= m_categories.size()) {
        return -1;
    }
    return m_categories.at(index).id;
}

QString CategoryModel::getCategoryName(int index) const
{
    if (index < 0 || index >= m_categories.size()) {
        return QString();
    }
    return m_categories.at(index).name;
}

} // namespace tosspos
