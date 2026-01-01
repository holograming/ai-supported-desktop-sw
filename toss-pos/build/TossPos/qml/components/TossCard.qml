import QtQuick
import "../theme"

Rectangle {
    id: root

    // Properties
    property bool hoverable: false
    property bool pressable: false
    property alias contentItem: contentContainer.data

    // Signals
    signal clicked()
    signal pressed()
    signal released()

    color: TossTheme.surface
    radius: TossTheme.radiusLg

    // Shadow effect
    layer.enabled: true
    layer.effect: Item {
        Rectangle {
            anchors.fill: parent
            anchors.margins: -1
            radius: root.radius + 1
            color: "transparent"
            border.width: 1
            border.color: TossTheme.border
        }
    }

    // Content container
    Item {
        id: contentContainer
        anchors.fill: parent
    }

    // Hover/Press overlay
    Rectangle {
        anchors.fill: parent
        radius: parent.radius
        color: mouseArea.pressed ? TossTheme.textPrimary :
               mouseArea.containsMouse ? TossTheme.textPrimary : "transparent"
        opacity: mouseArea.pressed ? 0.08 : mouseArea.containsMouse ? 0.04 : 0
        visible: root.hoverable || root.pressable

        Behavior on opacity {
            NumberAnimation { duration: TossTheme.animationFast }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        enabled: root.hoverable || root.pressable
        hoverEnabled: root.hoverable
        cursorShape: (root.hoverable || root.pressable) ? Qt.PointingHandCursor : Qt.ArrowCursor

        onClicked: root.clicked()
        onPressed: root.pressed()
        onReleased: root.released()
    }
}
