import QtQuick
import QtQuick.Layouts
import TossPos 1.0

Rectangle {
    id: root

    property int currentIndex: 0
    property var categories: []  // Array of {id, name}

    signal categorySelected(int categoryId, int index)

    color: TossTheme.surface
    radius: TossTheme.radiusMd

    implicitHeight: 56

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: TossTheme.spacingSm
        anchors.rightMargin: TossTheme.spacingSm
        spacing: TossTheme.spacingXs

        // "All" button
        CategoryTab {
            Layout.preferredHeight: 40
            text: "전체"
            isSelected: root.currentIndex === 0

            onClicked: {
                root.currentIndex = 0
                root.categorySelected(-1, 0)
            }
        }

        // Category buttons
        Repeater {
            model: root.categories

            CategoryTab {
                required property var modelData
                required property int index

                Layout.preferredHeight: 40
                text: modelData.name
                isSelected: root.currentIndex === index + 1

                onClicked: {
                    root.currentIndex = index + 1
                    root.categorySelected(modelData.id, index + 1)
                }
            }
        }

        // Spacer
        Item {
            Layout.fillWidth: true
        }
    }

    // Category tab component
    component CategoryTab: Rectangle {
        id: tabRoot

        property string text: ""
        property bool isSelected: false

        signal clicked()

        implicitWidth: tabText.implicitWidth + TossTheme.spacingLg * 2
        implicitHeight: 40
        radius: TossTheme.radiusMd

        color: isSelected ? TossTheme.primaryBlue :
               tabMouseArea.containsMouse ? TossTheme.surfaceHover : "transparent"

        Behavior on color {
            ColorAnimation { duration: TossTheme.animationFast }
        }

        Text {
            id: tabText
            anchors.centerIn: parent
            text: tabRoot.text
            font.pixelSize: TossTheme.fontSizeMd
            font.weight: tabRoot.isSelected ? Font.Bold : Font.Medium
            color: tabRoot.isSelected ? TossTheme.surface : TossTheme.textPrimary
        }

        MouseArea {
            id: tabMouseArea
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: tabRoot.clicked()
        }
    }
}
