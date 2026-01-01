pragma Singleton
import QtQuick

QtObject {
    // Colors - Toss Design System
    readonly property color primaryBlue: "#3182F6"
    readonly property color primaryBlueHover: "#1B64DA"
    readonly property color primaryBluePressed: "#1556C0"

    readonly property color textPrimary: "#191F28"
    readonly property color textSecondary: "#8B95A1"
    readonly property color textTertiary: "#B0B8C1"

    readonly property color background: "#F2F4F6"
    readonly property color surface: "#FFFFFF"
    readonly property color surfaceHover: "#F8F9FA"

    readonly property color success: "#03B26C"
    readonly property color successLight: "#E8F7F0"
    readonly property color error: "#F04452"
    readonly property color errorLight: "#FFEBEE"
    readonly property color warning: "#FF9500"

    readonly property color border: "#E5E8EB"
    readonly property color borderLight: "#F2F4F6"
    readonly property color divider: "#E5E8EB"

    // Card colors for products
    readonly property color cardCoffee: "#FFF5E6"
    readonly property color cardDrink: "#E6F4FF"
    readonly property color cardDessert: "#FFE6F0"
    readonly property color cardBakery: "#F0E6FF"

    // Spacing
    readonly property int spacingXs: 4
    readonly property int spacingSm: 8
    readonly property int spacingMd: 12
    readonly property int spacingLg: 16
    readonly property int spacingXl: 24
    readonly property int spacingXxl: 32

    // Border Radius
    readonly property int radiusSm: 6
    readonly property int radiusMd: 10
    readonly property int radiusLg: 16
    readonly property int radiusXl: 20
    readonly property int radiusFull: 9999

    // Typography
    readonly property int fontSizeXs: 11
    readonly property int fontSizeSm: 13
    readonly property int fontSizeMd: 15
    readonly property int fontSizeLg: 17
    readonly property int fontSizeXl: 20
    readonly property int fontSizeXxl: 24
    readonly property int fontSizeDisplay: 32

    // Shadows
    readonly property color shadowColor: "#1A000000"
    readonly property int shadowSm: 2
    readonly property int shadowMd: 4
    readonly property int shadowLg: 8

    // Animation
    readonly property int animationFast: 100
    readonly property int animationNormal: 200
    readonly property int animationSlow: 300

    // Button heights
    readonly property int buttonHeightSm: 36
    readonly property int buttonHeightMd: 44
    readonly property int buttonHeightLg: 52
    readonly property int buttonHeightXl: 60

    // Functions
    function formatPrice(price: int): string {
        return price.toLocaleString('ko-KR') + "원"
    }

    function getCategoryColor(index: int): color {
        var colors = [cardCoffee, cardDrink, cardDessert, cardBakery]
        return colors[index % colors.length]
    }
}
