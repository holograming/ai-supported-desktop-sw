#pragma once

#include <QString>

namespace tosspos {

struct Product
{
    int id{0};
    int categoryId{0};
    QString name;
    int price{0};
    QString imageUrl;
    bool isActive{true};
    int sortOrder{0};
};

struct Category
{
    int id{0};
    QString name;
    QString icon;
    int sortOrder{0};
};

} // namespace tosspos
