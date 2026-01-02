# 변경: 크로스 플랫폼 (Windows/macOS) 빌드 환경 자동화

## Why

TossPlace POS 프로젝트를 macOS와 Windows 모두에서 개발하기 위해서는:

1. **일관된 의존성 관리**: 각 개발자가 서로 다른 vcpkg 버전을 사용하면 빌드 오류 발생
2. **신규 개발자 온보딩**: 복잡한 수동 설정 제거 필요
3. **재현 가능한 빌드**: CI/CD와 로컬 빌드 환경 동일성 보장
4. **현재 문제점**:
   - vcpkg.json은 존재하나 CMakePresets.json 미설정
   - Windows 전용 대응 중 (macOS 고려 부족)
   - 각 플랫폼별 수동 경로 설정 필요

## What Changes

### 추가 사항
- ✅ **CMakePresets.json** (Windows/macOS 모두 지원)
- ✅ **vcpkg-configuration.json** (baseline 버전 관리)
- ✅ **build-scripts/setup-dev.sh** (macOS/Linux 자동 설정)
- ✅ **build-scripts/setup-dev.bat** (Windows 자동 설정)
- ✅ **BUILD.md** (크로스 플랫폼 빌드 가이드)
- ✅ **DEVELOPMENT.md** (개발자 온보딩 문서)

### 아키텍처

```
프로젝트 루트/
├── CMakeLists.txt               (기존, 수정 불필요)
├── CMakePresets.json            ← 추가 (플랫폼별 preset)
├── vcpkg.json                   (기존, manifest 모드)
├── vcpkg-configuration.json     ← 추가 (baseline 버전)
├── build-scripts/
│   ├── setup-dev.sh             ← 신규 (macOS/Linux)
│   └── setup-dev.bat            ← 신규 (Windows)
├── toss-pos/
│   └── CMakeLists.txt           (기존)
└── docs/
    ├── BUILD.md                 ← 신규 (빌드 가이드)
    └── DEVELOPMENT.md           ← 신규 (개발자 가이드)
```

## Impact

### 영향받는 스펙
- `toss-pos` (requirements)

### 영향받는 코드
- **추가**: 4개 파일 (CMakePresets.json, vcpkg-configuration.json, 2개 스크립트)
- **수정**: 0개 (기존 CMakeLists.txt 호환)
- **삭제**: 0개

### 신규 산출물
- **BUILD.md**: Windows/macOS 크로스 플랫폼 빌드 가이드
- **DEVELOPMENT.md**: 신규 개발자 온보딩 문서

## Technical Decisions

1. **vcpkg 관리 방식**: 하이브리드 (환경변수 + 자동 다운로드)
   - 저장소 크기 최소화 (vcpkg 미포함)
   - 자동화 수준 높음 (setup-dev 스크립트)
   - 버전 관리 명시적 (baseline hash)

2. **CMake 설정**: CMakePresets.json
   - Windows: Visual Studio 17 (MSVC)
   - macOS: Unix Makefiles (Apple Clang)
   - 플랫폼별 Triplet 자동 지정

3. **플랫폼별 Triplet**:
   - Windows x64: `x64-windows`
   - macOS Intel: `x64-osx`
   - macOS ARM64: `arm64-osx`

4. **초기 빌드 시간**: 30-60분 (Qt 6.5 첫 컴파일)
   - 이후 캐싱으로 5-10분으로 단축

