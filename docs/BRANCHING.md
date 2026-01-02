# Git 브랜치 전략

## 개요

이 프로젝트는 플랫폼별로 최적화된 브랜치 구조를 사용합니다:

- **main**: 플랫폼 독립적 코드 (Linux/macOS 호환)
- **windows**: Windows 전용 (vcpkg submodule 포함)
- **macos**: macOS 전용 (선택사항)

## main 브랜치

### 특징

- 플랫폼 독립적 소스 코드
- CMakeLists.txt, CMakePresets.json, setup-dev.sh/bat
- vcpkg.json (의존성 명시)
- **vcpkg 소스 코드 없음** (setup-dev.sh/bat이 자동 다운로드)
- 저장소 크기: < 50MB
- 모든 개발자가 사용 가능

### 빌드 방법

```bash
# 1. 개발 환경 자동 설정 (처음 한 번만)
./build-scripts/setup-dev.sh    # macOS/Linux
.\build-scripts\setup-dev.bat   # Windows

# 2. 새 터미널 열기 (또는 기존 터미널 재시작)

# 3. CMake 설정
cmake --preset <preset>
# 사용 가능한 preset:
# - windows-x64       (Windows Release)
# - windows-x64-debug (Windows Debug)
# - macos-x64         (macOS Intel Release)
# - macos-x64-debug   (macOS Intel Debug)
# - macos-arm64       (macOS ARM64 Release)
# - macos-arm64-debug (macOS ARM64 Debug)

# 4. 빌드
cmake --build --preset <preset> --config Release

# 5. 실행
./build/<preset>/toss-pos         # macOS
.\build\<preset>\toss-pos.exe     # Windows
```

### setup-dev 스크립트 작동 원리

```
setup-dev.sh/bat 실행
  ↓
Git/CMake 설치 여부 확인
  ↓
vcpkg가 이미 설치되어 있는지 확인
  ├─ 예: 기존 설치 유지 (git pull 대신 checkout만)
  └─ 아니오: GitHub에서 클론
  ↓
baseline hash로 명시적 체크아웃 (af752f21...)
  ↓
bootstrap-vcpkg.sh/bat 실행
  ↓
VCPKG_ROOT 환경 변수 설정 (영구)
```

**첫 설정 시 예상 시간**: 5-10분
**첫 빌드 시 예상 시간**: 30-60분 (Qt 6.5 컴파일)
**이후 빌드**: 5-10분 (캐시 사용)

---

## windows 브랜치

### 특징

- main 기반 + vcpkg submodule
- vcpkg/: Microsoft vcpkg 저장소의 git submodule
- .gitmodules: submodule 설정 파일
- **저장소 크기**: +500MB (vcpkg 포함)
- Windows 개발자 선택 사항

### 추천 대상

- Windows에서 주로 개발하는 개발자
- 빠른 빌드가 필요한 경우 (vcpkg 다운로드 시간 절감)
- 오프라인 환경에서 작업해야 하는 경우

### 클론 방법

```bash
# 방법 1: windows 브랜치로 직접 클론
git clone --branch windows https://github.com/your-org/toss-pos.git
cd toss-pos
git submodule update --init

# 방법 2: 기존 저장소에서 브랜치 전환
git clone https://github.com/your-org/toss-pos.git
cd toss-pos
git checkout windows
git submodule update --init
```

### 빌드 방법

```bash
# setup-dev.bat는 windows 브랜치에서도 동일하게 작동
# (vcpkg submodule이 존재하므로 빠르게 진행)
.\build-scripts\setup-dev.bat

# 이후는 main과 동일
cmake --preset windows-x64
cmake --build --preset windows-x64 --config Release
.\build\windows-x64\toss-pos.exe
```

### .gitmodules 내용

```
[submodule "vcpkg"]
  path = vcpkg
  url = https://github.com/microsoft/vcpkg.git
```

### submodule 업데이트

```bash
# 처음 초기화
git submodule update --init

# 나중에 업데이트 (최신 vcpkg 받기)
git submodule update --remote

# 특정 버전으로 고정 (baseline)
cd vcpkg
git checkout af752f21c9d79ba3df9cb0250ce2233933f58486
cd ..
git add vcpkg
git commit -m "Update vcpkg baseline"
```

---

## macos 브랜치 (선택사항)

### 계획

- macOS 특화 최적화
- Xcode 프로젝트 통합
- Apple Silicon 네이티브 빌드 캐싱

**현재 상태**: 계획 단계 (구현 안 됨)

---

## 개발 워크플로우

### 1. 일반 기능 개발 (main 브랜치 기반)

```bash
# 1. 최신 main 브랜치 가져오기
git checkout main
git pull origin main

# 2. 기능 브랜치 생성
git checkout -b feature/새기능

# 3. 코드 작성 및 테스트
# ... 코드 작성 ...
cmake --preset <preset>
cmake --build --preset <preset>
./build/<preset>/toss-pos

# 4. 커밋
git add .
git commit -m "feat: 새로운 기능 설명"

# 5. 푸시 및 PR
git push origin feature/새기능
# GitHub에서 Pull Request 생성
```

### 2. Windows 특화 개발

```bash
# 1. main에서 기능 개발 및 테스트
git checkout main
git checkout -b feature/windows기능
# ... 개발 ...

# 2. PR로 main에 병합
# ... main에서 테스트 완료 ...

# 3. windows 브랜치에 동기화
git checkout windows
git merge main

# 4. Windows 특화 수정 필요 시
git checkout -b feature/windows-specific
# ... Windows 특화 코드 ...
git commit -m "feat: Windows 특화 기능"

# 5. windows로 PR 또는 직접 병합
git checkout windows
git merge feature/windows-specific
git push origin windows
```

### 3. 버그 수정

```bash
# 모든 플랫폼에 영향을 주는 버그: main에서 수정
git checkout -b fix/버그설명
# ... 수정 ...
git push origin fix/버그설명
# Pull Request 생성

# Windows 전용 버그: windows에서 수정
git checkout windows
git checkout -b fix/windows버그
# ... 수정 ...
git push origin fix/windows버그
```

---

## CI/CD 자동화

### GitHub Actions 워크플로우

| 브랜치 | Workflow | 작동 | 실행 환경 |
|--------|----------|------|----------|
| main | ci-lint | JSON 검증 + .gitmodules 체크 | ubuntu-latest |
| main | build-macos | macOS Intel/ARM64 빌드 | macos-13, macos-14 |
| windows | build-windows | Windows x64 빌드 | windows-latest |

### 워크플로우 특징

**ci-lint.yml**: 모든 커밋에서 실행
- CMakePresets.json 형식 검증
- vcpkg.json 형식 검증
- .gitmodules가 main에 없음 확인

**build-macos.yml**: main 브랜치 푸시 시 실행
- macOS 13 (Intel) 빌드
- macOS 14 (Apple Silicon) 빌드
- Release/Debug 매트릭스 빌드
- 바이너리 artifact 생성

**build-windows.yml**: windows/main 브랜치 푸시 시 실행
- main 브랜치: vcpkg 자동 다운로드 후 빌드
- windows 브랜치: vcpkg submodule 사용 후 빌드
- Release/Debug 매트릭스 빌드
- 바이너리 artifact 생성

### 빌드 결과 확인

1. GitHub 저장소의 "Actions" 탭 열기
2. 최신 workflow 실행 선택
3. "Summary"에서 artifact 다운로드 가능 (30일 유지)

---

## 브랜치 동기화 전략

### main → windows 동기화

```bash
# 방법 1: Merge (권장 - 히스토리 유지)
git checkout windows
git merge main
git push origin windows

# 방법 2: Rebase (깨끗한 히스토리)
git checkout windows
git rebase main
git push origin windows --force-with-lease
```

### windows → main 동기화 (거의 하지 않음)

```bash
# windows에서 main으로 변경사항 가져오기
git checkout main
git merge windows
# 충돌 해결 (submodule 제거)
git rm .gitmodules vcpkg
git add .
git commit -m "Remove vcpkg submodule for main branch"
git push origin main
```

---

## 주의사항

### main 브랜치

- ❌ vcpkg 소스 코드를 **절대** 포함하지 마세요
- ❌ .gitmodules 파일을 **절대** 포함하지 마세요
- ✅ vcpkg.json (의존성 선언)은 포함하세요
- ✅ setup-dev.sh/bat 스크립트는 포함하세요

### windows 브랜치

- ✅ vcpkg를 git submodule로 포함하세요
- ✅ baseline hash 지정하여 버전 고정하세요
- ✅ 정기적으로 main과 동기화하세요

### 커밋 메시지

[Conventional Commits](https://www.conventionalcommits.org/) 형식 준수:

```
feat: 새로운 기능
fix: 버그 수정
refactor: 코드 리팩토링
test: 테스트 추가
docs: 문서 수정
chore: 빌드 설정, 의존성 관리
```

---

## 문제 해결

### Q: windows 브랜치와 main 브랜치의 차이점이 뭔가요?

**A**:
- main: 경량 (50MB 미만), 모든 플랫폼 호환
- windows: 무거움 (500MB 이상), Windows 개발 최적화
- 선택할 수 있으며, 필요에 따라 브랜치 전환 가능

### Q: submodule 업데이트 시 충돌이 발생했어요

```bash
git submodule update --init
# 또는
cd vcpkg
git checkout af752f21c9d79ba3df9cb0250ce2233933f58486
cd ..
git add vcpkg
git commit -m "Fix vcpkg submodule"
```

### Q: main에서 windows로 병합할 때 충돌이 발생했어요

```bash
git checkout windows
git merge main
# 충돌 발생: .gitmodules나 vcpkg 관련 파일은 무시
# (windows 버전 유지)
git checkout --theirs .gitmodules vcpkg
git add .
git commit -m "Merge main into windows"
```

### Q: windows 브랜치에서 실수로 .gitmodules를 삭제했어요

```bash
git checkout HEAD -- .gitmodules
git reset HEAD
# 또는 windows 브랜치 재생성
git branch -D windows
git checkout -b windows
git submodule add https://github.com/microsoft/vcpkg.git vcpkg
```

---

## 참고 자료

- [Git Submodules 공식 문서](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [CMakePresets.json 가이드](BUILD.md)
- [개발자 온보딩](DEVELOPMENT.md)
- [빌드 가이드](BUILD.md)

---

**마지막 업데이트**: 2026년 1월 2일

