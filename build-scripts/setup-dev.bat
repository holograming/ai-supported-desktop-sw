@echo off
REM ===================================================================
REM TossPlace POS - Windows Development Environment Setup
REM ===================================================================
REM
REM 목적: Windows에서 vcpkg를 자동으로 설치하고 환경 변수 설정
REM 필수 요구사항: Git, CMake 4.2.0+
REM
REM 사용법:
REM   .\build-scripts\setup-dev.bat
REM
REM ===================================================================

setlocal enabledelayedexpansion

REM 색상 정의 (선택사항)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RESET=[0m"

REM vcpkg baseline 버전 (모든 개발자가 동일한 버전 사용)
set "BASELINE_HASH=af752f21c9d79ba3df9cb0250ce2233933f58486"

REM 기본 vcpkg 경로 (사용자가 VCPKG_ROOT를 이미 설정한 경우 그것을 사용)
if not defined VCPKG_ROOT (
    set "VCPKG_ROOT=C:\vcpkg"
)

echo.
echo ===================================================================
echo TossPlace POS - Windows Development Environment Setup
echo ===================================================================
echo.
echo VCPKG_ROOT: %VCPKG_ROOT%
echo.

REM ===================================================================
REM Step 1: Git 설치 여부 확인
REM ===================================================================
echo [1/4] Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git not found. Please install Git first.
    echo Download: https://git-scm.com/download/win
    exit /b 1
)
echo OK: Git is installed
echo.

REM ===================================================================
REM Step 2: CMake 설치 여부 확인
REM ===================================================================
echo [2/4] Checking CMake installation...
cmake --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: CMake not found. Please install CMake 4.2.0 or later.
    echo Download: https://cmake.org/download/
    exit /b 1
)
echo OK: CMake is installed
echo.

REM ===================================================================
REM Step 3: vcpkg 설치 또는 업데이트
REM ===================================================================
echo [3/4] Setting up vcpkg...

if exist "%VCPKG_ROOT%" (
    echo vcpkg already exists at %VCPKG_ROOT%
) else (
    echo Cloning vcpkg from GitHub...
    git clone https://github.com/Microsoft/vcpkg.git "%VCPKG_ROOT%"
    if errorlevel 1 (
        echo ERROR: Failed to clone vcpkg
        exit /b 1
    )
)

REM Checkout baseline hash to ensure reproducible builds
echo Checking out baseline: %BASELINE_HASH%
cd /d "%VCPKG_ROOT%"
git checkout "%BASELINE_HASH%" >nul 2>&1
cd /d %~dp0..

REM Bootstrap vcpkg if not already done
if not exist "%VCPKG_ROOT%\vcpkg.exe" (
    echo Bootstrapping vcpkg...
    cd /d "%VCPKG_ROOT%"
    call bootstrap-vcpkg.bat
    if errorlevel 1 (
        echo ERROR: Failed to bootstrap vcpkg
        exit /b 1
    )
    cd /d %~dp0..
)
echo OK: vcpkg is ready
echo.

REM ===================================================================
REM Step 4: 환경 변수 설정
REM ===================================================================
echo [4/4] Setting environment variables...

REM 현재 세션에서 설정
set "VCPKG_ROOT=%VCPKG_ROOT%"

REM 영구적으로 설정 (모든 미래 터미널에서 사용 가능)
setx VCPKG_ROOT "%VCPKG_ROOT%"
if errorlevel 1 (
    echo WARNING: Failed to set environment variable permanently
    echo Please manually add VCPKG_ROOT to system environment variables
) else (
    echo OK: VCPKG_ROOT set to %VCPKG_ROOT%
)
echo.

REM ===================================================================
REM 완료 메시지
REM ===================================================================
echo ===================================================================
echo SETUP COMPLETE!
echo ===================================================================
echo.
echo Next steps:
echo.
echo 1. Open new command prompt or restart your shell
echo.
echo 2. Navigate to the project directory:
echo    cd toss-pos
echo.
echo 3. Configure and build:
echo    cmake --preset windows-x64
echo    cmake --build --preset windows-release
echo.
echo 4. Run the application:
echo    .\build\windows-x64\toss-pos.exe
echo.
echo For more information, see BUILD.md
echo.
echo ===================================================================
echo.

endlocal
