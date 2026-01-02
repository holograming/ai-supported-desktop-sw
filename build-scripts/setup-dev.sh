#!/bin/bash
# ===================================================================
# TossPlace POS - macOS/Linux Development Environment Setup
# ===================================================================
#
# 목적: macOS/Linux에서 vcpkg를 자동으로 설치하고 환경 변수 설정
# 필수 요구사항: Git, CMake 4.2.0+, Apple Clang (macOS) / GCC (Linux)
#
# 사용법:
#   ./build-scripts/setup-dev.sh
#
# ===================================================================

set -e

# 색상 정의 (터미널 출력용)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# vcpkg baseline 버전 (모든 개발자가 동일한 버전 사용)
BASELINE_HASH="af752f21c9d79ba3df9cb0250ce2233933f58486"

# 기본 vcpkg 경로 (사용자가 VCPKG_ROOT를 이미 설정한 경우 그것을 사용)
VCPKG_ROOT="${VCPKG_ROOT:-$HOME/vcpkg}"

echo ""
echo "==================================================================="
echo "TossPlace POS - macOS/Linux Development Environment Setup"
echo "==================================================================="
echo ""
echo "VCPKG_ROOT: $VCPKG_ROOT"
echo ""

# ===================================================================
# Step 1: Git 설치 여부 확인
# ===================================================================
echo "[1/4] Checking Git installation..."
if ! command -v git &> /dev/null; then
    echo -e "${RED}ERROR: Git not found.${NC} Please install Git first."
    echo "macOS: brew install git"
    echo "Linux: sudo apt-get install git"
    exit 1
fi
echo -e "${GREEN}OK: Git is installed${NC}"
echo ""

# ===================================================================
# Step 2: CMake 설치 여부 확인
# ===================================================================
echo "[2/4] Checking CMake installation..."
if ! command -v cmake &> /dev/null; then
    echo -e "${RED}ERROR: CMake not found.${NC} Please install CMake 4.2.0 or later."
    echo "macOS: brew install cmake"
    echo "Linux: sudo apt-get install cmake"
    exit 1
fi

CMAKE_VERSION=$(cmake --version | head -n1 | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')
echo "CMake version: $CMAKE_VERSION"
echo -e "${GREEN}OK: CMake is installed${NC}"
echo ""

# ===================================================================
# Step 3: vcpkg 설치 또는 업데이트
# ===================================================================
echo "[3/4] Setting up vcpkg..."

if [ -d "$VCPKG_ROOT" ]; then
    echo "vcpkg already exists at $VCPKG_ROOT"
else
    echo "Cloning vcpkg from GitHub..."
    git clone https://github.com/Microsoft/vcpkg.git "$VCPKG_ROOT"
fi

# Checkout baseline hash to ensure reproducible builds
echo "Checking out baseline: $BASELINE_HASH"
git -C "$VCPKG_ROOT" checkout "$BASELINE_HASH" 2>/dev/null || echo "Already on baseline"

# Bootstrap vcpkg if not already done
if [ ! -f "$VCPKG_ROOT/vcpkg" ]; then
    echo "Bootstrapping vcpkg..."
    cd "$VCPKG_ROOT"
    ./bootstrap-vcpkg.sh
    cd - > /dev/null
fi

echo -e "${GREEN}OK: vcpkg is ready${NC}"
echo ""

# ===================================================================
# Step 4: 환경 변수 설정
# ===================================================================
echo "[4/4] Setting environment variables..."

# 현재 세션에서 설정
export VCPKG_ROOT

# 향후 세션에서 자동 설정되도록 shell rc 파일에 추가
SHELL_PROFILE=""
if [ -f "$HOME/.bashrc" ]; then
    SHELL_PROFILE="$HOME/.bashrc"
elif [ -f "$HOME/.zshrc" ]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [ -f "$HOME/.profile" ]; then
    SHELL_PROFILE="$HOME/.profile"
fi

if [ -n "$SHELL_PROFILE" ]; then
    # 이미 설정되어 있는지 확인
    if ! grep -q "export VCPKG_ROOT" "$SHELL_PROFILE"; then
        echo "" >> "$SHELL_PROFILE"
        echo "# TossPlace POS - vcpkg" >> "$SHELL_PROFILE"
        echo "export VCPKG_ROOT='$VCPKG_ROOT'" >> "$SHELL_PROFILE"
        echo "✓ Added VCPKG_ROOT to $SHELL_PROFILE"
    else
        echo "✓ VCPKG_ROOT already configured in $SHELL_PROFILE"
    fi
else
    echo -e "${YELLOW}WARNING: Could not find shell profile (.bashrc, .zshrc, or .profile)${NC}"
    echo "Please manually add the following to your shell profile:"
    echo "  export VCPKG_ROOT='$VCPKG_ROOT'"
fi

echo -e "${GREEN}OK: Environment variables configured${NC}"
echo ""

# ===================================================================
# 완료 메시지
# ===================================================================
echo "==================================================================="
echo "SETUP COMPLETE!"
echo "==================================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Reload your shell configuration:"
echo "   source $SHELL_PROFILE"
echo "   OR close and reopen your terminal"
echo ""
echo "2. Navigate to the project directory:"
echo "   cd toss-pos"
echo ""
echo "3. Configure and build:"
echo "   # For macOS Intel:"
echo "   cmake --preset macos-x64"
echo "   cmake --build --preset macos-x64"
echo ""
echo "   # For macOS ARM64 (Apple Silicon M1/M2/M3):"
echo "   cmake --preset macos-arm64"
echo "   cmake --build --preset macos-arm64"
echo ""
echo "4. Run the application:"
echo "   ./build/macos-x64/toss-pos       (Intel)"
echo "   ./build/macos-arm64/toss-pos     (ARM64)"
echo ""
echo "For more information, see BUILD.md"
echo ""
echo "==================================================================="
echo ""
