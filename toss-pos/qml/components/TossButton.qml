import QtQuick
import QtQuick.Controls
import TossPos 1.0

Button {
    id: root

    // Custom properties
    property string variant: "primary" // primary, secondary, text, success, danger
    property bool loading: false

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: TossTheme.buttonHeightLg

    leftPadding: TossTheme.spacingLg
    rightPadding: TossTheme.spacingLg

    font.pixelSize: TossTheme.fontSizeMd
    font.weight: Font.Medium

    enabled: !loading

    contentItem: Item {
        implicitWidth: buttonText.implicitWidth + (loadingIndicator.visible ? loadingIndicator.width + TossTheme.spacingSm : 0)
        implicitHeight: buttonText.implicitHeight

        Row {
            anchors.centerIn: parent
            spacing: TossTheme.spacingSm

            // Loading indicator
            Rectangle {
                id: loadingIndicator
                width: 16
                height: 16
                radius: 8
                color: "transparent"
                border.width: 2
                border.color: getTextColor()
                visible: root.loading

                Rectangle {
                    width: 6
                    height: 6
                    radius: 3
                    color: getTextColor()
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 2
                }

                RotationAnimation on rotation {
                    running: loadingIndicator.visible
                    from: 0
                    to: 360
                    duration: 1000
                    loops: Animation.Infinite
                }
            }

            Text {
                id: buttonText
                text: root.text
                font: root.font
                color: getTextColor()
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }
    }

    background: Rectangle {
        implicitWidth: 100
        implicitHeight: root.implicitHeight
        radius: TossTheme.radiusMd
        color: getBackgroundColor()
        border.width: root.variant === "secondary" ? 1 : 0
        border.color: root.variant === "secondary" ? TossTheme.border : "transparent"

        Behavior on color {
            ColorAnimation { duration: TossTheme.animationFast }
        }
    }

    function getBackgroundColor() {
        if (!root.enabled) {
            return TossTheme.borderLight
        }

        switch (root.variant) {
        case "primary":
            return root.pressed ? TossTheme.primaryBluePressed :
                   root.hovered ? TossTheme.primaryBlueHover : TossTheme.primaryBlue
        case "secondary":
            return root.pressed ? TossTheme.border :
                   root.hovered ? TossTheme.surfaceHover : TossTheme.surface
        case "text":
            return root.pressed ? TossTheme.borderLight :
                   root.hovered ? TossTheme.surfaceHover : "transparent"
        case "success":
            return root.pressed ? Qt.darker(TossTheme.success, 1.2) :
                   root.hovered ? Qt.darker(TossTheme.success, 1.1) : TossTheme.success
        case "danger":
            return root.pressed ? Qt.darker(TossTheme.error, 1.2) :
                   root.hovered ? Qt.darker(TossTheme.error, 1.1) : TossTheme.error
        default:
            return TossTheme.primaryBlue
        }
    }

    function getTextColor() {
        if (!root.enabled) {
            return TossTheme.textTertiary
        }

        switch (root.variant) {
        case "primary":
        case "success":
        case "danger":
            return TossTheme.surface
        case "secondary":
        case "text":
            return TossTheme.textPrimary
        default:
            return TossTheme.surface
        }
    }
}
