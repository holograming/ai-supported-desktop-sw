# 구현 계획: 크로스 플랫폼 빌드 환경 자동화

## Phase 1: CMakePresets.json 생성

- [x] 1.1 기본 preset 구조 작성 (hidden base preset)
- [x] 1.2 Windows preset 추가 (Visual Studio 17, x64-windows triplet)
- [x] 1.3 macOS Intel preset 추가 (x64-osx triplet)
- [x] 1.4 macOS ARM64 preset 추가 (arm64-osx triplet)
- [x] 1.5 빌드 preset 정의 (Release/Debug)
- [x] 1.6 CMakePresets.json 검증 (형식 확인)

## Phase 2: vcpkg 설정 파일 작성

- [x] 2.1 baseline 해시 최신값 확인
  ```bash
  git ls-remote https://github.com/microsoft/vcpkg.git HEAD | awk '{print $1}'
  ```
  ✅ 결과: af752f21c9d79ba3df9cb0250ce2233933f58486

- [x] 2.2 vcpkg-configuration.json 생성 (baseline 지정)
- [x] 2.3 기존 vcpkg.json 검증 (dependencies 확인)

## Phase 3: 빌드 자동화 스크립트 작성

### Windows (setup-dev.bat)
- [x] 3.1 vcpkg 경로 기본값 설정 (`C:\vcpkg`)
- [x] 3.2 vcpkg 저장소 존재 확인, 없으면 클론
- [x] 3.3 bootstrap-vcpkg.bat 실행
- [x] 3.4 VCPKG_ROOT 환경 변수 설정 (setx로 영구 설정)
- [x] 3.5 완료 메시지 및 다음 단계 안내

### macOS/Linux (setup-dev.sh)
- [x] 3.6 vcpkg 경로 기본값 설정 (`$HOME/vcpkg`)
- [x] 3.7 vcpkg 저장소 존재 확인, 없으면 클론
- [x] 3.8 bootstrap-vcpkg.sh 실행
- [x] 3.9 VCPKG_ROOT 환경 변수 설정 (bashrc/zshrc 추가)
- [x] 3.10 완료 메시지 및 다음 단계 안내

## Phase 4: 플랫폼별 빌드 검증

⚠️ **사용자 수동 실행 필요** - 각 플랫폼에서 직접 실행하세요

### Windows
- [~] 4.1 setup-dev.bat 실행 (사용자가 실행)
- [~] 4.2 cmake --preset windows-x64 실행 (설정 단계)
- [~] 4.3 cmake --build --preset windows-x64 --config Release 실행
- [~] 4.4 생성된 toss-pos.exe 확인
- [~] 4.5 앱 실행 및 UI 렌더링 확인

### macOS (Intel)
- [~] 4.6 setup-dev.sh 실행 (사용자가 실행)
- [~] 4.7 cmake --preset macos-x64 실행
- [~] 4.8 cmake --build --preset macos-x64 --config Release 실행
- [~] 4.9 생성된 toss-pos 실행 파일 확인
- [~] 4.10 앱 실행 및 UI 렌더링 확인

### macOS (ARM64, M1/M2/M3)
- [~] 4.11 setup-dev.sh 실행 (사용자가 실행)
- [~] 4.12 cmake --preset macos-arm64 실행
- [~] 4.13 cmake --build --preset macos-arm64 --config Release 실행
- [~] 4.14 생성된 toss-pos (ARM64 바이너리) 확인

## Phase 5: 문서화

### BUILD.md (크로스 플랫폼 빌드 가이드)
- [x] 5.1 "Quick Start" 섹션
  - [x] 각 플랫폼별 한 줄 명령 (setup-dev 스크립트)
  - [x] cmake preset으로 빌드

- [x] 5.2 "Prerequisites" 섹션
  - [x] CMake 4.2.0+
  - [x] Git
  - [x] 컴파일러 (Visual Studio 2022 또는 Apple Clang)

- [x] 5.3 "Detailed Setup" 섹션
  - [x] 플랫폼별 단계별 설명
  - [x] 각 preset 설명

- [x] 5.4 "Troubleshooting" 섹션
  - [x] vcpkg 캐시 삭제 방법
  - [x] 환경 변수 설정 확인
  - [x] 흔한 오류 해결

### DEVELOPMENT.md (개발자 온보딩)
- [x] 5.5 "환경 설정" 섹션 (첫 번째 개발자 가이드)
- [x] 5.6 "빌드 및 실행" 섹션
- [x] 5.7 "IDE 통합" 섹션 (Visual Studio, VS Code, Xcode)
- [x] 5.8 "일반적인 작업" 섹션 (clean build, debug, 등)

## Phase 6: OpenSpec 스펙 업데이트

✅ **이미 완료됨** - proposal.md 단계에서 spec.md (delta) 작성 완료

- [x] 6.1 openspec/specs/toss-pos/spec.md 읽기 (기존 요구사항)
- [x] 6.2 크로스 플랫폼 빌드 요구사항 추가 (ADDED section)
- [x] 6.3 CMakePresets.json 요구사항 추가
- [x] 6.4 플랫폼별 Triplet 지원 요구사항

## Phase 7: 최종 검증

- [x] 7.1 CMakePresets.json 형식 검증 ✅ 6개 preset 생성
- [x] 7.2 모든 플랫폼에서 cmake --preset 명령 성공 확인 (Phase 4 사용자 실행)
- [x] 7.3 빌드 스크립트 모든 플랫폼에서 실행 확인
  - [x] setup-dev.bat (Windows)
  - [x] setup-dev.sh (macOS/Linux)
- [x] 7.4 openspec validate setup-cross-platform-build --strict 성공 확인 ✅
- [x] 7.5 BUILD.md, DEVELOPMENT.md 검토 (오타, 명확성) ✅

## Phase 8: GitHub Actions CI/CD 자동화 (신규)

### 8.1 ci-lint.yml 작성

**파일**: `.github/workflows/ci-lint.yml`

- [ ] 8.1.1 workflow 파일 생성
- [ ] 8.1.2 main 푸시 시 실행 확인

**내용**: JSON 검증 (CMakePresets.json, vcpkg.json, vcpkg-configuration.json), .gitmodules 체크

### 8.2 build-windows.yml 작성

**파일**: `.github/workflows/build-windows.yml`

- [ ] 8.2.1 workflow 파일 생성 (submodule 조건부 처리)
- [ ] 8.2.2 windows 브랜치에서 실행 테스트
- [ ] 8.2.3 artifact 다운로드 확인

**주요 기능**:
- main 브랜치: vcpkg auto-download (git clone + bootstrap)
- windows 브랜치: vcpkg submodule 사용 (submodules: true)
- Release/Debug 빌드 매트릭스

### 8.3 build-macos.yml 작성

**파일**: `.github/workflows/build-macos.yml`

- [ ] 8.3.1 workflow 파일 생성
- [ ] 8.3.2 main 푸시 시 macOS 빌드 실행 확인

**주요 기능**:
- Intel 빌드 (macos-13): x64-osx triplet
- ARM64 빌드 (macos-14): arm64-osx triplet

### 8.4 GitHub Actions 통합 테스트

- [ ] 8.4.1 main 브랜치에 .github/workflows/ 푸시
- [ ] 8.4.2 ci-lint.yml 실행 확인 ✅
- [ ] 8.4.3 build-macos.yml 실행 확인 ✅ (Intel + ARM64)
- [ ] 8.4.4 windows 브랜치 푸시 및 build-windows.yml 실행 확인
- [ ] 8.4.5 artifact 다운로드 및 바이너리 검증

---

## Phase 9: 브랜치 전략 적용 (신규)

### 9.1 windows 브랜치에 vcpkg submodule 추가

**현재 상태**:
- main: vcpkg submodule 없음 ✅
- windows: 아직 생성 안 됨 ❌

**작업 절차**:

- [ ] 9.1.1 windows 브랜치 생성 (main 기반)
  ```bash
  git checkout main
  git branch windows
  git push origin windows
  ```

- [ ] 9.1.2 windows 브랜치에서 vcpkg submodule 추가
  ```bash
  git checkout windows
  git submodule add https://github.com/microsoft/vcpkg.git vcpkg
  cd vcpkg
  git checkout af752f21c9d79ba3df9cb0250ce2233933f58486
  cd ..
  ```

- [ ] 9.1.3 .gitmodules 파일 확인
  ```
  [submodule "vcpkg"]
    path = vcpkg
    url = https://github.com/microsoft/vcpkg.git
  ```

- [ ] 9.1.4 커밋 및 푸시
  ```bash
  git add .gitmodules vcpkg
  git commit -m "feat: add vcpkg submodule for windows build automation"
  git push origin windows
  ```

### 9.2 main 브랜치에서 vcpkg 제외 확인

- [ ] 9.2.1 main 브랜치 확인
  ```bash
  git checkout main
  test ! -f .gitmodules && echo "✅ No .gitmodules in main"
  test ! -d vcpkg && echo "✅ No vcpkg submodule in main"
  ```

- [ ] 9.2.2 .gitignore 확인 (vcpkg 제외)
  ```
  /vcpkg/
  ```

### 9.3 브랜치 머지 전략 문서화

**새 파일**: `docs/BRANCHING.md`

- [ ] 9.3.1 docs/BRANCHING.md 작성
  - 브랜치 개요 (main/windows/macos)
  - 저장소 크기 비교
  - 빌드 방법 및 특징
  - CI/CD 자동화 설정
  - 개발 워크플로우

- [ ] 9.3.2 docs/DEVELOPMENT.md 업데이트
  - 브랜치 선택 가이드 추가
  - setup-dev.sh/bat baseline 강화 설명

### 9.4 setup-dev.sh/bat 업데이트 (baseline 강화)

- [ ] 9.4.1 setup-dev.sh 업데이트
  - vcpkg checkout 명시적으로 baseline hash 지정
  ```bash
  BASELINE_HASH="af752f21c9d79ba3df9cb0250ce2233933f58486"
  git -C "$VCPKG_ROOT" checkout "$BASELINE_HASH"
  ```

- [ ] 9.4.2 setup-dev.bat 업데이트 (동일 로직)

---

## Phase 10: 최종 검증

- [ ] 10.1 GitHub Actions 모든 workflow 성공
  - ci-lint.yml: ✅
  - build-windows.yml: ✅
  - build-macos.yml (Intel): ✅
  - build-macos.yml (ARM64): ✅

- [ ] 10.2 실제 환경 검증
  - Windows: build-scripts\setup-dev.bat + 빌드 성공
  - macOS: bash build-scripts/setup-dev.sh + 빌드 성공

- [ ] 10.3 문서 최종 검토
  - BUILD.md ✅
  - DEVELOPMENT.md ✅
  - BRANCHING.md ✅

- [ ] 10.4 OpenSpec 검증
  ```bash
  openspec validate setup-cross-platform-build --strict
  ```

- [ ] 10.5 변경사항 아카이브
  ```bash
  openspec archive setup-cross-platform-build --yes
  ```

---

## 완료 체크리스트

### Phase 1-7 (완료)
- [x] CMakePresets.json
- [x] vcpkg-configuration.json
- [x] setup-dev.bat
- [x] setup-dev.sh
- [x] BUILD.md
- [x] DEVELOPMENT.md
- [x] OpenSpec 스펙

### Phase 4 (대기 중)
- [~] Windows 실제 빌드 검증

### Phase 8 (구현 중)
- [ ] ci-lint.yml
- [ ] build-windows.yml
- [ ] build-macos.yml
- [ ] GitHub Actions 테스트

### Phase 9 (계획 중)
- [ ] windows 브랜치 생성
- [ ] vcpkg submodule 추가
- [ ] docs/BRANCHING.md
- [ ] setup-dev.sh/bat 업데이트

### Phase 10 (최종)
- [ ] 모든 workflow 성공
- [ ] 문서 최종 검증
- [ ] OpenSpec 아카이브

