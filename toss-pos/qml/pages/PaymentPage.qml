import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import TossPos 1.0

Item {
    id: root

    // Properties
    property string paymentType: "CARD"  // "CARD" or "CASH"
    property int totalAmount: OrderModel.totalAmount

    // Signals
    signal paymentCompleted()
    signal paymentCancelled()

    Rectangle {
        anchors.fill: parent
        color: TossTheme.background
    }

    // Main content - centered
    ColumnLayout {
        anchors.centerIn: parent
        width: Math.min(480, parent.width - TossTheme.spacingXxl * 2)
        spacing: TossTheme.spacingXl

        // Back button
        TossButton {
            Layout.alignment: Qt.AlignLeft
            text: "< 뒤로"
            variant: "text"
            implicitHeight: TossTheme.buttonHeightMd

            onClicked: root.paymentCancelled()
        }

        // Payment card
        TossCard {
            Layout.fillWidth: true
            Layout.preferredHeight: 400

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: TossTheme.spacingXl
                spacing: TossTheme.spacingXl

                // Title
                Text {
                    Layout.alignment: Qt.AlignHCenter
                    text: root.paymentType === "CARD" ? "카드 결제" : "현금 결제"
                    font.pixelSize: TossTheme.fontSizeXl
                    font.weight: Font.Bold
                    color: TossTheme.textPrimary
                }

                // Amount
                ColumnLayout {
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter
                    spacing: TossTheme.spacingSm

                    Text {
                        Layout.alignment: Qt.AlignHCenter
                        text: "결제 금액"
                        font.pixelSize: TossTheme.fontSizeMd
                        color: TossTheme.textSecondary
                    }

                    Text {
                        Layout.alignment: Qt.AlignHCenter
                        text: TossTheme.formatPrice(root.totalAmount)
                        font.pixelSize: TossTheme.fontSizeDisplay
                        font.weight: Font.Bold
                        color: TossTheme.primaryBlue
                    }
                }

                // Order summary
                TossCard {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 120

                    ListView {
                        anchors.fill: parent
                        anchors.margins: TossTheme.spacingMd
                        clip: true
                        spacing: TossTheme.spacingXs
                        model: OrderModel

                        delegate: RowLayout {
                            required property string productName
                            required property int quantity
                            required property int subtotal

                            width: parent ? parent.width : 0

                            Text {
                                Layout.fillWidth: true
                                text: productName + " x " + quantity
                                font.pixelSize: TossTheme.fontSizeSm
                                color: TossTheme.textSecondary
                                elide: Text.ElideRight
                            }

                            Text {
                                text: TossTheme.formatPrice(subtotal)
                                font.pixelSize: TossTheme.fontSizeSm
                                color: TossTheme.textSecondary
                            }
                        }
                    }
                }

                Item { Layout.fillHeight: true }

                // Payment instruction
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 60
                    radius: TossTheme.radiusMd
                    color: root.paymentType === "CARD" ? TossTheme.primaryBlue : TossTheme.success
                    opacity: 0.1

                    Text {
                        anchors.centerIn: parent
                        text: root.paymentType === "CARD" ?
                              "카드를 리더기에 삽입해주세요" :
                              "현금을 받고 결제를 완료해주세요"
                        font.pixelSize: TossTheme.fontSizeMd
                        font.weight: Font.Medium
                        color: root.paymentType === "CARD" ? TossTheme.primaryBlue : TossTheme.success
                    }
                }

                // Action buttons
                RowLayout {
                    Layout.fillWidth: true
                    spacing: TossTheme.spacingMd

                    TossButton {
                        Layout.fillWidth: true
                        text: "취소"
                        variant: "secondary"

                        onClicked: root.paymentCancelled()
                    }

                    TossButton {
                        Layout.fillWidth: true
                        text: "결제 완료"
                        variant: root.paymentType === "CARD" ? "primary" : "success"

                        onClicked: {
                            if (OrderService.processPayment(root.paymentType)) {
                                successDialog.orderNo = OrderService.getLastOrderNo()
                                successDialog.totalAmount = OrderService.getLastOrderTotal()
                                successDialog.open()
                            }
                        }
                    }
                }
            }
        }
    }

    // Success dialog
    Dialog {
        id: successDialog
        anchors.centerIn: parent
        width: 360
        modal: true
        closePolicy: Popup.NoAutoClose

        property string orderNo: ""
        property int totalAmount: 0

        background: Rectangle {
            color: TossTheme.surface
            radius: TossTheme.radiusLg
        }

        contentItem: ColumnLayout {
            spacing: TossTheme.spacingLg

            // Success icon
            Rectangle {
                Layout.alignment: Qt.AlignHCenter
                width: 64
                height: 64
                radius: 32
                color: TossTheme.successLight

                Text {
                    anchors.centerIn: parent
                    text: "V"
                    font.pixelSize: TossTheme.fontSizeXxl
                    font.weight: Font.Bold
                    color: TossTheme.success
                }
            }

            Text {
                Layout.alignment: Qt.AlignHCenter
                text: "결제 완료"
                font.pixelSize: TossTheme.fontSizeXl
                font.weight: Font.Bold
                color: TossTheme.textPrimary
            }

            // Order info
            ColumnLayout {
                Layout.fillWidth: true
                spacing: TossTheme.spacingSm

                RowLayout {
                    Layout.fillWidth: true
                    Text {
                        text: "주문번호"
                        font.pixelSize: TossTheme.fontSizeMd
                        color: TossTheme.textSecondary
                    }
                    Item { Layout.fillWidth: true }
                    Text {
                        text: successDialog.orderNo
                        font.pixelSize: TossTheme.fontSizeMd
                        font.weight: Font.Medium
                        color: TossTheme.textPrimary
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    Text {
                        text: "결제금액"
                        font.pixelSize: TossTheme.fontSizeMd
                        color: TossTheme.textSecondary
                    }
                    Item { Layout.fillWidth: true }
                    Text {
                        text: TossTheme.formatPrice(successDialog.totalAmount)
                        font.pixelSize: TossTheme.fontSizeMd
                        font.weight: Font.Bold
                        color: TossTheme.primaryBlue
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    Text {
                        text: "결제수단"
                        font.pixelSize: TossTheme.fontSizeMd
                        color: TossTheme.textSecondary
                    }
                    Item { Layout.fillWidth: true }
                    Text {
                        text: root.paymentType === "CARD" ? "카드" : "현금"
                        font.pixelSize: TossTheme.fontSizeMd
                        font.weight: Font.Medium
                        color: TossTheme.textPrimary
                    }
                }
            }

            TossButton {
                Layout.fillWidth: true
                Layout.topMargin: TossTheme.spacingMd
                text: "확인"
                variant: "primary"

                onClicked: {
                    successDialog.close()
                    root.paymentCompleted()
                }
            }
        }
    }

    // Error handling
    Connections {
        target: OrderService
        function onPaymentFailed(message) {
            errorDialog.message = message
            errorDialog.open()
        }
    }

    // Error dialog
    Dialog {
        id: errorDialog
        anchors.centerIn: parent
        width: 320
        modal: true
        title: "결제 오류"

        property string message: ""

        background: Rectangle {
            color: TossTheme.surface
            radius: TossTheme.radiusLg
        }

        contentItem: ColumnLayout {
            spacing: TossTheme.spacingMd

            Text {
                Layout.fillWidth: true
                text: errorDialog.message
                font.pixelSize: TossTheme.fontSizeMd
                color: TossTheme.error
                wrapMode: Text.WordWrap
            }

            TossButton {
                Layout.fillWidth: true
                text: "확인"
                variant: "primary"
                onClicked: errorDialog.close()
            }
        }
    }
}
