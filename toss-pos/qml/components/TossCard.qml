import QtQuick
import TossPos 1.0

Item {
    id: root

    // Properties
    property bool hoverable: false
    property bool pressable: false
    property alias contentItem: cardContent.data

    // Signals
    signal clicked()
    signal pressed()
    signal released()

    // Shadow layers (simulated drop shadow)
    Rectangle {
        id: shadowOuter
        anchors.fill: card
        anchors.margins: -1
        anchors.topMargin: 2
        anchors.leftMargin: 1
        radius: card.radius + 2
        color: "#08000000"  // 3% opacity black
    }

    Rectangle {
        id: shadowMiddle
        anchors.fill: card
        anchors.margins: -1
        anchors.topMargin: 4
        anchors.leftMargin: 2
        radius: card.radius + 2
        color: "#06000000"  // 2% opacity black
    }

    Rectangle {
        id: shadowInner
        anchors.fill: card
        anchors.topMargin: 1
        radius: card.radius + 1
        color: "#04000000"  // 1.5% opacity black
    }

    // Main card
    Rectangle {
        id: card
        anchors.fill: parent
        color: TossTheme.surface
        radius: TossTheme.radiusLg
        border.width: 1
        border.color: TossTheme.border

        // Content container
        Item {
            id: cardContent
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
