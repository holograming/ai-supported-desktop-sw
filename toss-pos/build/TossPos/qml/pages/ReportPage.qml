import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import TossPos 1.0
import "../theme"
import "../components"

Item {
    id: root

    // Signals
    signal navigateBack()

    Rectangle {
        anchors.fill: parent
        color: TossTheme.background
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: TossTheme.spacingLg
        spacing: TossTheme.spacingLg

        // Header
        RowLayout {
            Layout.fillWidth: true

            TossButton {
                text: "< 뒤로"
                variant: "text"
                implicitHeight: TossTheme.buttonHeightMd
                onClicked: root.navigateBack()
            }

            Text {
                Layout.fillWidth: true
                text: "매출 조회"
                font.pixelSize: TossTheme.fontSizeXxl
                font.weight: Font.Bold
                color: TossTheme.textPrimary
                horizontalAlignment: Text.AlignHCenter
            }

            // Placeholder for symmetry
            Item { width: 80 }
        }

        // Date navigation
        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: TossTheme.spacingLg

            TossButton {
                text: "<"
                variant: "secondary"
                implicitWidth: 44
                implicitHeight: TossTheme.buttonHeightMd
                onClicked: ReportService.previousDay()
            }

            Text {
                text: ReportService.formatDate(ReportService.currentDate)
                font.pixelSize: TossTheme.fontSizeLg
                font.weight: Font.Medium
                color: TossTheme.textPrimary
            }

            TossButton {
                text: ">"
                variant: "secondary"
                implicitWidth: 44
                implicitHeight: TossTheme.buttonHeightMd
                enabled: ReportService.currentDate < new Date()
                onClicked: ReportService.nextDay()
            }

            TossButton {
                text: "오늘"
                variant: "text"
                implicitHeight: TossTheme.buttonHeightMd
                onClicked: ReportService.goToToday()
            }
        }

        // Summary cards
        RowLayout {
            Layout.fillWidth: true
            spacing: TossTheme.spacingMd

            // Total sales
            SummaryCard {
                Layout.fillWidth: true
                title: "총 매출"
                value: TossTheme.formatPrice(ReportService.totalSales)
                valueColor: TossTheme.primaryBlue
                iconText: "$"
                iconColor: TossTheme.primaryBlue
            }

            // Order count
            SummaryCard {
                Layout.fillWidth: true
                title: "주문 건수"
                value: ReportService.orderCount + "건"
                valueColor: TossTheme.textPrimary
                iconText: "#"
                iconColor: TossTheme.success
            }

            // Cash sales
            SummaryCard {
                Layout.fillWidth: true
                title: "현금 결제"
                value: TossTheme.formatPrice(ReportService.cashSales)
                valueColor: TossTheme.success
                iconText: "W"
                iconColor: TossTheme.success
            }

            // Card sales
            SummaryCard {
                Layout.fillWidth: true
                title: "카드 결제"
                value: TossTheme.formatPrice(ReportService.cardSales)
                valueColor: TossTheme.primaryBlue
                iconText: "C"
                iconColor: TossTheme.primaryBlue
            }
        }

        // Order list
        TossCard {
            Layout.fillWidth: true
            Layout.fillHeight: true

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: TossTheme.spacingLg
                spacing: TossTheme.spacingMd

                Text {
                    text: "주문 내역"
                    font.pixelSize: TossTheme.fontSizeLg
                    font.weight: Font.Bold
                    color: TossTheme.textPrimary
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 1
                    color: TossTheme.divider
                }

                ListView {
                    id: orderListView
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    spacing: TossTheme.spacingSm
                    model: ReportService.orders

                    // Empty state
                    Text {
                        anchors.centerIn: parent
                        visible: orderListView.count === 0
                        text: "주문 내역이 없습니다"
                        font.pixelSize: TossTheme.fontSizeMd
                        color: TossTheme.textTertiary
                    }

                    delegate: OrderHistoryItem {
                        required property var modelData
                        width: orderListView.width
                        orderNo: modelData.orderNo
                        time: modelData.createdAt
                        total: modelData.total
                        paymentType: modelData.paymentType
                        items: modelData.items
                    }

                    ScrollBar.vertical: ScrollBar {
                        policy: ScrollBar.AsNeeded
                    }
                }
            }
        }
    }

    // Summary card component
    component SummaryCard: TossCard {
        id: summaryCard

        property string title: ""
        property string value: ""
        property color valueColor: TossTheme.textPrimary
        property string iconText: ""
        property color iconColor: TossTheme.primaryBlue

        implicitHeight: 100

        RowLayout {
            anchors.fill: parent
            anchors.margins: TossTheme.spacingMd
            spacing: TossTheme.spacingMd

            // Icon
            Rectangle {
                width: 48
                height: 48
                radius: TossTheme.radiusMd
                color: Qt.rgba(summaryCard.iconColor.r, summaryCard.iconColor.g, summaryCard.iconColor.b, 0.1)

                Text {
                    anchors.centerIn: parent
                    text: summaryCard.iconText
                    font.pixelSize: TossTheme.fontSizeXl
                    font.weight: Font.Bold
                    color: summaryCard.iconColor
                }
            }

            ColumnLayout {
                Layout.fillWidth: true
                spacing: TossTheme.spacingXs

                Text {
                    text: summaryCard.title
                    font.pixelSize: TossTheme.fontSizeSm
                    color: TossTheme.textSecondary
                }

                Text {
                    text: summaryCard.value
                    font.pixelSize: TossTheme.fontSizeXl
                    font.weight: Font.Bold
                    color: summaryCard.valueColor
                }
            }
        }
    }

    // Order history item component
    component OrderHistoryItem: TossCard {
        id: historyItem

        property string orderNo: ""
        property string time: ""
        property int total: 0
        property string paymentType: ""
        property var items: []

        implicitHeight: expanded ? 80 + itemsColumn.height : 80
        hoverable: true

        property bool expanded: false

        Behavior on implicitHeight {
            NumberAnimation { duration: TossTheme.animationNormal }
        }

        onClicked: expanded = !expanded

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: TossTheme.spacingMd
            spacing: TossTheme.spacingSm

            RowLayout {
                Layout.fillWidth: true
                spacing: TossTheme.spacingMd

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: TossTheme.spacingXs

                    Text {
                        text: historyItem.orderNo
                        font.pixelSize: TossTheme.fontSizeMd
                        font.weight: Font.Medium
                        color: TossTheme.textPrimary
                    }

                    Text {
                        text: historyItem.time
                        font.pixelSize: TossTheme.fontSizeSm
                        color: TossTheme.textSecondary
                    }
                }

                // Payment type badge
                Rectangle {
                    width: badgeText.implicitWidth + TossTheme.spacingMd
                    height: 24
                    radius: 12
                    color: historyItem.paymentType === "CARD" ?
                           Qt.rgba(TossTheme.primaryBlue.r, TossTheme.primaryBlue.g, TossTheme.primaryBlue.b, 0.1) :
                           Qt.rgba(TossTheme.success.r, TossTheme.success.g, TossTheme.success.b, 0.1)

                    Text {
                        id: badgeText
                        anchors.centerIn: parent
                        text: historyItem.paymentType === "CARD" ? "카드" : "현금"
                        font.pixelSize: TossTheme.fontSizeXs
                        font.weight: Font.Medium
                        color: historyItem.paymentType === "CARD" ? TossTheme.primaryBlue : TossTheme.success
                    }
                }

                Text {
                    text: TossTheme.formatPrice(historyItem.total)
                    font.pixelSize: TossTheme.fontSizeLg
                    font.weight: Font.Bold
                    color: TossTheme.textPrimary
                }

                Text {
                    text: historyItem.expanded ? "^" : "v"
                    font.pixelSize: TossTheme.fontSizeMd
                    color: TossTheme.textTertiary
                }
            }

            // Expanded items
            ColumnLayout {
                id: itemsColumn
                Layout.fillWidth: true
                visible: historyItem.expanded
                spacing: TossTheme.spacingXs

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 1
                    color: TossTheme.divider
                }

                Repeater {
                    model: historyItem.items

                    RowLayout {
                        required property var modelData
                        Layout.fillWidth: true

                        Text {
                            Layout.fillWidth: true
                            text: modelData.productName + " x " + modelData.quantity
                            font.pixelSize: TossTheme.fontSizeSm
                            color: TossTheme.textSecondary
                        }

                        Text {
                            text: TossTheme.formatPrice(modelData.subtotal)
                            font.pixelSize: TossTheme.fontSizeSm
                            color: TossTheme.textSecondary
                        }
                    }
                }
            }
        }
    }
}
