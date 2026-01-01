import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import TossPos 1.0

Item {
    id: root

    // Signals
    signal navigateToPayment(string paymentType)
    signal navigateToReport()

    // Current category (-1 = all)
    property int currentCategoryId: -1
    property int currentCategoryIndex: 0

    // Build category list from model
    function getCategoryList() {
        var list = []
        for (var i = 0; i < CategoryModel.count; i++) {
            list.push({
                id: CategoryModel.getCategoryId(i),
                name: CategoryModel.getCategoryName(i)
            })
        }
        return list
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: TossTheme.spacingLg
        spacing: TossTheme.spacingLg

        // Left section - Products (70%)
        ColumnLayout {
            Layout.fillHeight: true
            Layout.preferredWidth: parent.width * 0.68
            spacing: TossTheme.spacingMd

            // Header
            RowLayout {
                Layout.fillWidth: true

                Text {
                    text: "TossPlace POS"
                    font.pixelSize: TossTheme.fontSizeXxl
                    font.weight: Font.Bold
                    color: TossTheme.textPrimary
                }

                Item { Layout.fillWidth: true }

                // Report button
                TossButton {
                    text: "매출 조회"
                    variant: "text"
                    implicitHeight: TossTheme.buttonHeightMd

                    onClicked: root.navigateToReport()
                }
            }

            // Category bar
            CategoryBar {
                Layout.fillWidth: true
                categories: getCategoryList()
                currentIndex: root.currentCategoryIndex

                onCategorySelected: function(categoryId, index) {
                    root.currentCategoryId = categoryId
                    root.currentCategoryIndex = index
                    ProductModel.categoryId = categoryId
                }
            }

            // Product grid
            TossCard {
                Layout.fillWidth: true
                Layout.fillHeight: true

                GridView {
                    id: productGrid
                    anchors.fill: parent
                    anchors.margins: TossTheme.spacingMd
                    clip: true

                    cellWidth: 160
                    cellHeight: 170

                    model: ProductModel

                    delegate: ProductCard {
                        // index is auto-injected by model for delegate position
                        required property int index

                        width: productGrid.cellWidth - TossTheme.spacingSm
                        height: productGrid.cellHeight - TossTheme.spacingSm

                        categoryIndex: root.currentCategoryIndex > 0 ? root.currentCategoryIndex - 1 : index % 4

                        onAddToCart: {
                            OrderModel.addItem(productId, name, price)
                        }
                    }

                    // Empty state
                    Text {
                        anchors.centerIn: parent
                        visible: productGrid.count === 0
                        text: "등록된 상품이 없습니다"
                        font.pixelSize: TossTheme.fontSizeMd
                        color: TossTheme.textTertiary
                    }

                    ScrollBar.vertical: ScrollBar {
                        policy: ScrollBar.AsNeeded
                    }
                }
            }
        }

        // Right section - Order Panel (30%)
        OrderPanel {
            Layout.fillHeight: true
            Layout.preferredWidth: parent.width * 0.30

            model: OrderModel
            totalAmount: OrderModel.totalAmount
            itemCount: OrderModel.count
            isEmpty: OrderModel.isEmpty

            onPaymentRequested: function(paymentType) {
                root.navigateToPayment(paymentType)
            }

            onClearRequested: {
                clearDialog.open()
            }
        }
    }

    // Clear confirmation dialog
    Dialog {
        id: clearDialog
        anchors.centerIn: parent
        width: 320
        modal: true
        title: "주문 초기화"

        background: Rectangle {
            color: TossTheme.surface
            radius: TossTheme.radiusLg
        }

        contentItem: ColumnLayout {
            spacing: TossTheme.spacingMd

            Text {
                Layout.fillWidth: true
                text: "현재 주문 목록을 모두 삭제하시겠습니까?"
                font.pixelSize: TossTheme.fontSizeMd
                color: TossTheme.textPrimary
                wrapMode: Text.WordWrap
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.topMargin: TossTheme.spacingMd
                spacing: TossTheme.spacingMd

                TossButton {
                    Layout.fillWidth: true
                    text: "취소"
                    variant: "secondary"
                    implicitHeight: TossTheme.buttonHeightMd
                    onClicked: clearDialog.close()
                }

                TossButton {
                    Layout.fillWidth: true
                    text: "삭제"
                    variant: "danger"
                    implicitHeight: TossTheme.buttonHeightMd
                    onClicked: {
                        OrderModel.clear()
                        clearDialog.close()
                    }
                }
            }
        }
    }
}
