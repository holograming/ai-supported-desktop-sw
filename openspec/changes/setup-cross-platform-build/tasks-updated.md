# 구현 계획: 크로스 플랫폼 빌드 환경 자동화 (업데이트)

## 상태 요약

| Phase | 작업 | 상태 |
|-------|------|------|
| **1-3** | CMakePresets, vcpkg 설정, setup 스크립트 | ✅ 완료 |
| **5-7** | 문서화, 스펙 업데이트, 검증 | ✅ 완료 |
| **4** | Windows 실제 빌드 검증 | ⏳ 사용자 수동 |
| **8** | GitHub Actions CI/CD 자동화 | ⏳ 신규 구현 |
| **9** | 브랜치 전략 (main/windows) | ⏳ 신규 구현 |

---

## Phase 4: Windows 빌드 검증 (실제 환경)

⚠️ **사용자가 직접 Windows 환경에서 실행해야 함**

### 사전 준비
- [ ] Visual Studio 2022 설치 (Desktop development with C++)
- [ ] CMake 3.25+ 설치
- [ ] Git 설치
- [ ] 인터넷 연결 (vcpkg 다운로드용)

### 단계별 실행

#### Step 1: 프로젝트 준비
```cmd
git clone <repo-url>
cd toss-pos
```

#### Step 2: 개발 환경 설정
```cmd
build-scripts\setup-dev.bat
```
**예상 시간**: 5-10분
**결과**: VCPKG_ROOT=C:\vcpkg 설정 + vcpkg 다운로드

#### Step 3: 새 Command Prompt 열기
- [~] 4.1 새 터미널에서 환경 변수 확인
  ```cmd
  echo %VCPKG_ROOT%
  rem 결과: C:\vcpkg
  ```

#### Step 4: CMake 구성
- [~] 4.2 cmake --list-presets 실행
- [~] 4.3 cmake --preset windows-x64 실행
  ```cmd
  cd toss-pos
  cmake --preset windows-x64
  ```
  **예상 시간**: 10-30분 (vcpkg 의존성 다운로드)
  **첫 빌드**: +30분 (Qt 6.5 컴파일)

#### Step 5: 빌드
- [~] 4.4 빌드 시작
  ```cmd
  cmake --build --preset windows-x64 --config Release
  ```
  **예상 시간**: 10-30분

#### Step 6: 검증
- [~] 4.5 실행 파일 확인
  ```cmd
  dir build\windows-x64\Release\toss-pos.exe
  ```

- [~] 4.6 앱 실행
  ```cmd
  .\build\windows-x64\Release\toss-pos.exe
  ```
  **검증 항목**:
  - [ ] 윈도우 창 열림
  - [ ] QML UI 렌더링 (토스 디자인 시스템)
  - [ ] 카테고리 탭 표시
  - [ ] 상품 그리드 표시
  - [ ] 주문 패널 표시 (카드 스타일)

---

## Phase 8: GitHub Actions CI/CD 자동화 (신규)

### 8.1 ci-lint.yml 작성

**파일**: `.github/workflows/ci-lint.yml`

```yaml
name: Code Lint & Static Analysis

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate CMakePresets.json
        run: python3 -m json.tool CMakePresets.json > /dev/null

      - name: Validate vcpkg files
        run: |
          python3 -m json.tool vcpkg.json > /dev/null
          python3 -m json.tool vcpkg-configuration.json > /dev/null

      - name: Check .gitmodules not in main
        run: test ! -f .gitmodules && echo "✅ .gitmodules not in main"
```

- [x] 8.1.1 workflow 파일 생성
- [ ] 8.1.2 main 푸시 시 실행 확인

### 8.2 build-windows.yml 작성

**파일**: `.github/workflows/build-windows.yml`

```yaml
name: Build Windows

on:
  push:
    branches: [windows, main]
  pull_request:
    branches: [windows, main]

env:
  VCPKG_ROOT: C:\vcpkg

jobs:
  build:
    runs-on: windows-latest
    strategy:
      matrix:
        config: [Release, Debug]

    steps:
      - uses: actions/checkout@v4
        with:
          submodules: ${{ contains(github.ref, 'windows') }}

      - name: Setup vcpkg (main 브랜치)
        if: ${{ !contains(github.ref, 'windows') }}
        run: |
          git clone https://github.com/microsoft/vcpkg.git ${{ env.VCPKG_ROOT }}
          cd ${{ env.VCPKG_ROOT }}
          git checkout af752f21c9d79ba3df9cb0250ce2233933f58486
          .\bootstrap-vcpkg.bat

      - name: Setup vcpkg (windows 브랜치, submodule 사용)
        if: ${{ contains(github.ref, 'windows') }}
        run: |
          cd vcpkg
          .\bootstrap-vcpkg.bat

      - name: Configure CMake
        run: cmake --preset windows-x64

      - name: Build
        run: cmake --build --preset windows-x64 --config ${{ matrix.config }}

      - name: Upload Artifact
        if: matrix.config == 'Release'
        uses: actions/upload-artifact@v3
        with:
          name: toss-pos-windows-x64-${{ matrix.config }}
          path: build/windows-x64/${{ matrix.config }}/toss-pos.exe
          retention-days: 30
```

- [ ] 8.2.1 workflow 파일 생성
- [ ] 8.2.2 windows 브랜치에서 실행 테스트
- [ ] 8.2.3 artifact 다운로드 확인

### 8.3 build-macos.yml 작성

**파일**: `.github/workflows/build-macos.yml`

```yaml
name: Build macOS

on:
  push:
    branches: [main, macos]
  pull_request:
    branches: [main, macos]

jobs:
  build-intel:
    runs-on: macos-13  # Intel
    strategy:
      matrix:
        config: [Release, Debug]

    steps:
      - uses: actions/checkout@v4

      - name: Setup vcpkg
        run: bash build-scripts/setup-dev.sh

      - name: Configure CMake
        run: cmake --preset macos-x64

      - name: Build
        run: cmake --build --preset macos-x64 --config ${{ matrix.config }}

      - name: Upload Artifact
        if: matrix.config == 'Release'
        uses: actions/upload-artifact@v3
        with:
          name: toss-pos-macos-x64-${{ matrix.config }}
          path: build/macos-x64/${{ matrix.config }}/toss-pos
          retention-days: 30

  build-arm64:
    runs-on: macos-14  # Apple Silicon
    strategy:
      matrix:
        config: [Release, Debug]

    steps:
      - uses: actions/checkout@v4

      - name: Setup vcpkg
        run: bash build-scripts/setup-dev.sh

      - name: Configure CMake
        run: cmake --preset macos-arm64

      - name: Build
        run: cmake --build --preset macos-arm64 --config ${{ matrix.config }}

      - name: Upload Artifact
        if: matrix.config == 'Release'
        uses: actions/upload-artifact@v3
        with:
          name: toss-pos-macos-arm64-${{ matrix.config }}
          path: build/macos-arm64/${{ matrix.config }}/toss-pos
          retention-days: 30
```

- [ ] 8.3.1 workflow 파일 생성
- [ ] 8.3.2 main 푸시 시 macOS 빌드 실행 확인

### 8.4 GitHub Actions 통합 테스트

- [ ] 8.4.1 main 브랜치에 푸시
  ```bash
  git add .github/workflows/
  git commit -m "feat: add GitHub Actions CI/CD workflows"
  git push origin main
  ```

- [ ] 8.4.2 GitHub Actions 탭에서 workflow 실행 확인
  - ci-lint.yml: ✅ 통과
  - build-macos.yml: ✅ 통과 (Intel + ARM64)

- [ ] 8.4.3 windows 브랜치에 푸시
  ```bash
  git checkout windows
  git merge main
  git push origin windows
  ```

- [ ] 8.4.4 build-windows.yml 실행 확인
  - build-windows.yml: ✅ 통과

- [ ] 8.4.5 artifact 다운로드 및 테스트
  - Windows: toss-pos.exe 실행
  - macOS: toss-pos 실행

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

```markdown
# Git 브랜치 전략

## 개요

이 프로젝트는 플랫폼별로 최적화된 브랜치 구조를 사용합니다:
- **main**: 플랫폼 독립적 코드
- **windows**: Windows 전용 (vcpkg submodule 포함)
- **macos**: macOS 전용 (선택)

## main 브랜치

- 플랫폼 독립적 소스 코드
- CMakeLists.txt, CMakePresets.json, setup-dev.sh/bat
- vcpkg.json (의존성 명시)
- setup-dev.sh/bat이 자동으로 vcpkg 다운로드
- 저장소 크기: < 50MB
- 모든 개발자가 사용

### 빌드 방법
```bash
bash build-scripts/setup-dev.sh  # macOS
build-scripts\setup-dev.bat      # Windows
cmake --preset <preset>
cmake --build --preset <preset>
```

## windows 브랜치

- main 기반 + vcpkg submodule
- vcpkg/: git submodule (Microsoft/vcpkg)
- .gitmodules: submodule 설정
- 저장소 크기: +500MB (vcpkg 포함)
- Windows 개발자 선택 사항

### 빌드 방법
```bash
git clone --branch windows <repo>
git submodule update --init
build-scripts\setup-dev.bat
cmake --preset windows-x64
cmake --build --preset windows-x64
```

## 개발 워크플로우

### 일반 기능 개발
```
main에서 브랜치 생성
→ 기능 개발
→ Pull Request
→ CI/CD 테스트 (ci-lint + build-macos)
→ merge to main
```

### Windows 특화 개발
```
main에서 기능 개발
→ windows로 merge (rebase 또는 merge)
→ build-windows.yml 자동 테스트
→ 필요시 Windows 특화 수정
```

## CI/CD 자동화

| 브랜치 | Workflow | 동작 |
|--------|----------|------|
| main | ci-lint | JSON 검증 + 포맷 체크 |
| main | build-macos | macOS Intel/ARM64 빌드 |
| windows | build-windows | Windows x64 빌드 |

## 주의사항

- main에는 vcpkg 소스 코드를 **절대 포함하지 마세요**
- windows 브랜치는 main에서 최신 상태로 유지하세요
- submodule 충돌 시: `git submodule update --init`
```

- [ ] 9.3.1 docs/BRANCHING.md 작성
- [ ] 9.3.2 DEVELOPMENT.md 업데이트 (브랜치 선택 가이드)

### 9.4 setup-dev.sh/bat 업데이트 (baseline 강화)

**setup-dev.sh** 개선사항:

```bash
#!/bin/bash
set -e

BASELINE_HASH="af752f21c9d79ba3df9cb0250ce2233933f58486"
VCPKG_ROOT="${VCPKG_ROOT:=$HOME/vcpkg}"

echo "📦 TossPlace POS - vcpkg Setup"
echo "   Location: $VCPKG_ROOT"
echo "   Baseline: $BASELINE_HASH"

if [ ! -d "$VCPKG_ROOT" ]; then
  echo "   → Cloning..."
  git clone https://github.com/microsoft/vcpkg.git "$VCPKG_ROOT"
fi

echo "   → Checking out baseline..."
git -C "$VCPKG_ROOT" checkout "$BASELINE_HASH"

echo "   → Bootstrapping..."
"$VCPKG_ROOT/bootstrap-vcpkg.sh"

export VCPKG_ROOT
echo "✅ Ready: cmake --preset <preset>"
```

- [ ] 9.4.1 setup-dev.sh 업데이트
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

