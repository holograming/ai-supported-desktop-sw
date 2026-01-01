import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import TossPos 1.0
import "theme"
import "pages"

ApplicationWindow {
    id: window

    visible: true
    width: 1280
    height: 720
    minimumWidth: 1024
    minimumHeight: 600
    title: qsTr("TossPlace POS")

    // Background color
    color: TossTheme.background

    // Page stack
    StackView {
        id: stackView
        anchors.fill: parent
        initialItem: orderPageComponent
    }

    // Order page component
    Component {
        id: orderPageComponent

        OrderPage {
            onNavigateToPayment: function(paymentType) {
                stackView.push(paymentPageComponent, { paymentType: paymentType })
            }

            onNavigateToReport: {
                ReportService.refresh()
                stackView.push(reportPageComponent)
            }
        }
    }

    // Payment page component
    Component {
        id: paymentPageComponent

        PaymentPage {
            onPaymentCompleted: {
                stackView.pop()
            }

            onPaymentCancelled: {
                stackView.pop()
            }
        }
    }

    // Report page component
    Component {
        id: reportPageComponent

        ReportPage {
            onNavigateBack: {
                stackView.pop()
            }
        }
    }

    // Global keyboard shortcuts
    Shortcut {
        sequence: "Escape"
        onActivated: {
            if (stackView.depth > 1) {
                stackView.pop()
            }
        }
    }

    // F1: Go to order page
    Shortcut {
        sequence: "F1"
        onActivated: {
            stackView.pop(null)  // Pop to first item
        }
    }

    // F2: Go to report page
    Shortcut {
        sequence: "F2"
        onActivated: {
            if (stackView.currentItem.objectName !== "reportPage") {
                ReportService.refresh()
                stackView.push(reportPageComponent)
            }
        }
    }
}
