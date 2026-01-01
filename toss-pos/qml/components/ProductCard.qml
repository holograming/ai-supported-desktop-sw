import QtQuick
import QtQuick.Layouts
import "../theme"

TossCard {
    id: root

    // Required properties
    required property int productId
    required property string name
    required property int price
    property int categoryIndex: 0

    // Signals
    signal addToCart()

    implicitWidth: 150
    implicitHeight: 160
    hoverable: true
    pressable: true

    onClicked: root.addToCart()

    // Content
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: TossTheme.spacingMd
        spacing: TossTheme.spacingSm

        // Product icon/color area
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 70
            radius: TossTheme.radiusMd
            color: TossTheme.getCategoryColor(root.categoryIndex)

            // Product initial
            Text {
                anchors.centerIn: parent
                text: root.name.charAt(0)
                font.pixelSize: TossTheme.fontSizeXxl
                font.weight: Font.Bold
                color: TossTheme.textPrimary
                opacity: 0.6
            }
        }

        // Product name
        Text {
            Layout.fillWidth: true
            text: root.name
            font.pixelSize: TossTheme.fontSizeMd
            font.weight: Font.Medium
            color: TossTheme.textPrimary
            elide: Text.ElideRight
            maximumLineCount: 1
        }

        // Price
        Text {
            Layout.fillWidth: true
            text: TossTheme.formatPrice(root.price)
            font.pixelSize: TossTheme.fontSizeSm
            font.weight: Font.DemiBold
            color: TossTheme.primaryBlue
        }
    }

    // Scale animation on press (using TossCard's internal mouseArea via pressed signal)
    property bool isPressed: false
    scale: isPressed ? 0.96 : 1.0

    onPressed: isPressed = true
    onReleased: isPressed = false

    Behavior on scale {
        NumberAnimation { duration: TossTheme.animationFast }
    }
}
