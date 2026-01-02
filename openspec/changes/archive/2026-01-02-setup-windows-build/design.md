# Windows 빌드 환경 구축 - 기술 설계

## 컨텍스트

### 배경
- TossPlace POS 프로젝트는 원래 macOS 환경에서 개발됨 (CMakeLists.txt에 macOS 번들 설정 포함)
- 이제 Windows 환경으로 확장해야 하며, 기존 macOS 빌드 호환성 유지 필요
- Qt 6.5+ 및 의존성 관리를 자동화해야 함

### 제약사항
- **프로젝트 구조**: Qt6 + QML 기반 데스크톱 앱
- **의존성**: sqlite3, spdlog (vcpkg.json에 선언됨)
- **빌드 도구**: CMake 3.25+ 요구 (이미 설치됨)
- **컴파일러**: Windows MSVC 2022 사용
- **플랫폼**: Windows 10+, macOS 11+ 모두 지원 필요

### 이해관계자
- 개발자: Windows 환경에서 빠른 빌드 필요
- DevOps (인재): 향후 CI/CD 자동화 필요

---

## 목표 / 비목표

### 목표
1. **Windows 빌드 자동화**: vcpkg manifest mode를 활용한 의존성 자동 설치
2. **개발자 경험 개선**: 명확한 빌드 가이드 제공 (BUILD_WINDOWS.md)
3. **크로스 플랫폼 호환성**: 기존 macOS 빌드 유지, 향후 Linux 지원 가능하도록
4. **빌드 재현성**: 모든 Windows 개발자가 동일한 환경 구축 가능

### 비목표
- GitHub Actions CI/CD 자동화 (이 변경에서는 수동 빌드만 지원)
- Linux 빌드 지원 (향후 변경으로 미루기)
- IDE 통합 설정 (VS Code, Visual Studio 프리셋은 선택사항)
- 자동 버전 관리 (vcpkg는 항상 최신 버전 사용)

---

## 결정

### 1. vcpkg 사용 (Manifest Mode)
**결정**: 프로젝트에 이미 `vcpkg.json`이 있으므로 manifest mode를 사용한다.

**근거**:
- ✅ 프로젝트 소스 코드 내에 의존성 선언 (일관성)
- ✅ 개발자마다 다른 버전 관리 불필요
- ✅ CI/CD와 로컬 빌드 환경 동일

**대안 검토**:
- ❌ 수동 Qt 설치 (너무 복잡, 버전 관리 어려움)
- ❌ Conan (오버 엔지니어링, 이미 vcpkg.json 있음)

---

### 2. vcpkg 설치 위치: `C:\vcpkg`
**결정**: vcpkg를 `C:\vcpkg`에 설치한다.

**근거**:
- ✅ 표준 위치 (대부분 Windows 개발자가 예상)
- ✅ 경로 간단 (공백 없음)
- ✅ 환경 변수 설정 불필요

**대안 검토**:
- ❌ `C:\Program Files\vcpkg` (경로 길고 공백 있음)
- ❌ 사용자별 로컬 설치 (일관성 부족)

---

### 3. CMake 설정 방식: 수동 `-D` 플래그
**결정**: CMake 설정 시 `-DCMAKE_TOOLCHAIN_FILE`을 수동으로 전달한다.

```bash
cmake -S . -B build `
  -DCMAKE_TOOLCHAIN_FILE=C:\vcpkg\scripts\buildsystems\vcpkg.cmake `
  -DVCPKG_TARGET_TRIPLET=x64-windows
```

**근거**:
- ✅ 직관적이고 명시적
- ✅ 환경 변수 의존 불필요
- ✅ 빌드 재현성 높음

**대안 검토**:
- 🔲 CMakePresets.json (자동화, 이후 개선으로 추가 가능)
- 🔲 환경 변수 `CMAKE_TOOLCHAIN_FILE` (암묵적, 오류 가능성 높음)

---

### 4. 빌드 스크립트 제공 (선택사항)
**결정**: `build_windows.bat` 및/또는 `build_windows.ps1` 제공 (필수는 아님).

**근거**:
- ✅ 초기 세팅 자동화 가능
- ✅ 신규 개발자 온보딩 용이
- ✅ 재현 가능한 빌드 환경

---

## 위험 / 트레이드오프

### 위험 1: vcpkg 빌드 시간
**문제**: Qt 6.5를 처음 빌드할 때 **30-60분** 소요 가능
**완화 방법**:
- 개발자 가이드에 "시간 소요 예상" 명시
- 이후 빌드는 캐시로 빠름

### 위험 2: 경로 길이 제한 (Windows)
**문제**: vcpkg 빌드 중간 생성 파일 경로가 260자를 초과할 수 있음 (Windows 경로 제한)
**완화 방법**:
- `C:\vcpkg` (단순 경로) 사용으로 최소화
- CMakeLists.txt에 상대 경로만 사용

### 위험 3: macOS 호환성 유지
**문제**: Windows 캐시와 macOS 캐시 충돌 가능
**완화 방법**:
- `build/` 디렉토리를 플랫폼별로 분리 (향후: `build-windows/`, `build-macos/`)
- 지금은 명시적으로 "다시 생성" 권고

---

## 마이그레이션 계획

### Phase 1: vcpkg 설치 (Task 2)
```bash
git clone https://github.com/Microsoft/vcpkg.git C:\vcpkg
cd C:\vcpkg
.\bootstrap-vcpkg.bat
```

### Phase 2: CMake 설정 (Task 3)
```bash
cd toss-pos
rm -rf build && mkdir build
cmake -S . -B build `
  -DCMAKE_TOOLCHAIN_FILE=C:\vcpkg\scripts\buildsystems\vcpkg.cmake `
  -DVCPKG_TARGET_TRIPLET=x64-windows
```

### Phase 3: 빌드 및 테스트 (Tasks 4-5)
```bash
cmake --build build --config Release
.\build\Release\toss-pos.exe
```

### Phase 4: 문서화 (Task 7)
- `BUILD_WINDOWS.md` 작성
- `openspec/specs/toss-pos/spec.md` 업데이트

---

## 열린 질문

1. **자동 빌드 스크립트**: `build_windows.bat` 또는 `build_windows.ps1` 제공 필요?
   - 현재: 선택사항 (Task 6)
   - 추천: Phase 2 완료 후 결정

2. **CMakePresets.json 사용**: IDE 통합 자동화?
   - 현재: 미포함
   - 추천: Visual Studio 2022 네이티브 지원 (추후 개선)

3. **Linux 빌드 지원**: 언제부터?
   - 현재: 로드맵 외
   - 추천: 별도 변경으로 `setup-linux-build` 진행

4. **CI/CD 통합**: GitHub Actions Windows 작업?
   - 현재: 로드맵 외 (Task 8)
   - 추천: Windows 빌드 검증 후 별도 변경으로 진행

