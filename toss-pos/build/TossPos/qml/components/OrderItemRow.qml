import QtQuick
import QtQuick.Layouts
import "../theme"

Rectangle {
    id: root

    // Required properties
    required property int index
    required property string productName
    required property int quantity
    required property int unitPrice
    required property int subtotal

    // Signals
    signal increaseClicked()
    signal decreaseClicked()
    signal removeClicked()

    implicitHeight: 64
    color: mouseArea.containsMouse ? TossTheme.surfaceHover : "transparent"
    radius: TossTheme.radiusSm

    Behavior on color {
        ColorAnimation { duration: TossTheme.animationFast }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
    }

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: TossTheme.spacingMd
        anchors.rightMargin: TossTheme.spacingMd
        spacing: TossTheme.spacingMd

        // Product info
        ColumnLayout {
            Layout.fillWidth: true
            spacing: TossTheme.spacingXs

            Text {
                text: root.productName
                font.pixelSize: TossTheme.fontSizeMd
                font.weight: Font.Medium
                color: TossTheme.textPrimary
                elide: Text.ElideRight
                Layout.fillWidth: true
            }

            Text {
                text: TossTheme.formatPrice(root.unitPrice)
                font.pixelSize: TossTheme.fontSizeSm
                color: TossTheme.textSecondary
            }
        }

        // Quantity controls
        Row {
            spacing: TossTheme.spacingSm

            // Decrease button
            Rectangle {
                width: 32
                height: 32
                radius: TossTheme.radiusSm
                color: decreaseMouseArea.containsMouse ? TossTheme.surfaceHover : TossTheme.borderLight
                border.width: 1
                border.color: TossTheme.border

                Text {
                    anchors.centerIn: parent
                    text: "-"
                    font.pixelSize: TossTheme.fontSizeLg
                    font.weight: Font.Medium
                    color: TossTheme.textPrimary
                }

                MouseArea {
                    id: decreaseMouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.decreaseClicked()
                }
            }

            // Quantity display
            Rectangle {
                width: 40
                height: 32
                color: "transparent"

                Text {
                    anchors.centerIn: parent
                    text: root.quantity
                    font.pixelSize: TossTheme.fontSizeMd
                    font.weight: Font.DemiBold
                    color: TossTheme.textPrimary
                }
            }

            // Increase button
            Rectangle {
                width: 32
                height: 32
                radius: TossTheme.radiusSm
                color: increaseMouseArea.containsMouse ? TossTheme.surfaceHover : TossTheme.borderLight
                border.width: 1
                border.color: TossTheme.border

                Text {
                    anchors.centerIn: parent
                    text: "+"
                    font.pixelSize: TossTheme.fontSizeLg
                    font.weight: Font.Medium
                    color: TossTheme.textPrimary
                }

                MouseArea {
                    id: increaseMouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.increaseClicked()
                }
            }
        }

        // Subtotal
        Text {
            Layout.preferredWidth: 80
            text: TossTheme.formatPrice(root.subtotal)
            font.pixelSize: TossTheme.fontSizeMd
            font.weight: Font.DemiBold
            color: TossTheme.textPrimary
            horizontalAlignment: Text.AlignRight
        }
    }
}
