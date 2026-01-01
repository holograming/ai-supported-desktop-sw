import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import TossPos 1.0

Rectangle {
    id: root

    // Properties
    property alias model: orderList.model
    property int totalAmount: 0
    property int itemCount: 0
    property bool isEmpty: itemCount === 0

    // Signals
    signal paymentRequested(string paymentType)
    signal clearRequested()

    color: TossTheme.surface
    radius: TossTheme.radiusLg

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: TossTheme.spacingLg
        spacing: 0

        // Header
        RowLayout {
            Layout.fillWidth: true
            Layout.bottomMargin: TossTheme.spacingMd

            Text {
                text: "주문 목록"
                font.pixelSize: TossTheme.fontSizeLg
                font.weight: Font.Bold
                color: TossTheme.textPrimary
            }

            Item { Layout.fillWidth: true }

            // Item count badge
            Rectangle {
                visible: root.itemCount > 0
                width: countText.implicitWidth + TossTheme.spacingMd
                height: 24
                radius: 12
                color: TossTheme.primaryBlue

                Text {
                    id: countText
                    anchors.centerIn: parent
                    text: root.itemCount + "건"
                    font.pixelSize: TossTheme.fontSizeSm
                    font.weight: Font.Medium
                    color: TossTheme.surface
                }
            }

            // Clear button
            Rectangle {
                visible: root.itemCount > 0
                width: 32
                height: 32
                radius: TossTheme.radiusSm
                color: clearMouseArea.containsMouse ? TossTheme.surfaceHover : "transparent"

                Text {
                    anchors.centerIn: parent
                    text: "X"
                    font.pixelSize: TossTheme.fontSizeMd
                    font.weight: Font.Medium
                    color: TossTheme.textSecondary
                }

                MouseArea {
                    id: clearMouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.clearRequested()
                }
            }
        }

        // Divider
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 1
            color: TossTheme.divider
        }

        // Order list
        ListView {
            id: orderList
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.topMargin: TossTheme.spacingSm
            clip: true
            spacing: TossTheme.spacingXs

            // Empty state
            Text {
                anchors.centerIn: parent
                visible: root.isEmpty
                text: "주문할 상품을 선택해주세요"
                font.pixelSize: TossTheme.fontSizeMd
                color: TossTheme.textTertiary
            }

            delegate: OrderItemRow {
                // Model injects directly into OrderItemRow's required properties
                width: orderList.width

                onIncreaseClicked: OrderModel.increaseQuantity(index)
                onDecreaseClicked: OrderModel.decreaseQuantity(index)
            }

            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AsNeeded
            }
        }

        // Divider
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 1
            Layout.topMargin: TossTheme.spacingSm
            color: TossTheme.divider
        }

        // Total section
        RowLayout {
            Layout.fillWidth: true
            Layout.topMargin: TossTheme.spacingMd

            Text {
                text: "총 결제금액"
                font.pixelSize: TossTheme.fontSizeLg
                font.weight: Font.Medium
                color: TossTheme.textPrimary
            }

            Item { Layout.fillWidth: true }

            Text {
                text: TossTheme.formatPrice(root.totalAmount)
                font.pixelSize: TossTheme.fontSizeXxl
                font.weight: Font.Bold
                color: TossTheme.primaryBlue
            }
        }

        // Payment buttons
        RowLayout {
            Layout.fillWidth: true
            Layout.topMargin: TossTheme.spacingLg
            spacing: TossTheme.spacingMd

            TossButton {
                Layout.fillWidth: true
                text: "현금 결제"
                variant: "secondary"
                enabled: !root.isEmpty

                onClicked: root.paymentRequested("CASH")
            }

            TossButton {
                Layout.fillWidth: true
                text: "카드 결제"
                variant: "primary"
                enabled: !root.isEmpty

                onClicked: root.paymentRequested("CARD")
            }
        }
    }
}
