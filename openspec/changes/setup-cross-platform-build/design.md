# 크로스 플랫폼 빌드 환경 자동화 - 기술 설계

## 컨텍스트

### 배경
- **현재 상황**: 프로젝트가 macOS 중심으로 개발되었으며, Windows 지원 요청
- **기술 스택**: Qt 6.5 + CMake 3.25+ (크로스 플랫폼 기본 지원)
- **팀 규모**: 소수 개발자 (1-3명) → 자동화 최우선
- **목표**: Mac/Windows 모두에서 **동일한 의존성 버전** + **자동화된 설정**

### 제약사항
- **저장소 크기**: 1GB 이상 증가 안 함 (vcpkg 미포함)
- **초기 빌드 시간**: 30-60분 (Qt 6.5 첫 컴파일) 인정
- **재현성**: baseline hash로 명시적 버전 관리 필수
- **호환성**: 기존 CMakeLists.txt 수정 최소화

### 이해관계자
- **개발자**: Windows/macOS에서 빠른 온보딩 필요
- **DevOps (인재)**: 향후 CI/CD 자동화 고려
- **QA (지평)**: 모든 플랫폼에서 동일한 빌드 검증 필요

---

## 목표 / 비목표

### 목표 ✅
1. **플랫폼별 자동 설정**: CMakePresets.json으로 플랫폼 감지 후 자동 구성
2. **일관된 의존성**: vcpkg-configuration.json baseline으로 모든 개발자가 동일 버전
3. **간편한 온보딩**: `setup-dev.sh/bat` 한 줄 실행으로 vcpkg 설치 + 환경 변수 설정
4. **저장소 경량성**: vcpkg 소스 코드 미포함 (동적 다운로드)
5. **개발자 경험**: IDE 통합 (Visual Studio, VS Code, Xcode 네이티브 지원)

### 비목표 ❌
- GitHub Actions CI/CD 자동화 (이 변경에서 제외, 별도 변경)
- Linux 빌드 지원 (향후 `setup-linux-build` 변경)
- 바이너리 배포 (아직 시뮬레이션 환경)
- vcpkg 커스텀 포트 (표준 포트만 사용)

---

## 기술 결정

### 1. vcpkg 관리: 하이브리드 (환경변수 + 자동 다운로드)

**결정**:
```
├── 로컬 설치 위치
│   ├── Windows: C:\vcpkg
│   └── macOS: $HOME/vcpkg
├── 관리 방식: 환경 변수 (VCPKG_ROOT)
├── 자동화: setup-dev 스크립트가 자동으로 다운로드 + 설정
└── 버전 관리: vcpkg-configuration.json (baseline hash)
```

**근거**:
- ✅ 저장소 크기 최소화 (vcpkg 미포함)
- ✅ 자동화 수준 높음 (스크립트 1회만 실행)
- ✅ 재현성 높음 (baseline hash로 명시적 관리)
- ✅ 유연성 (개발자가 이미 설치된 vcpkg 사용 가능)

**대안 검토**:
```
1. Git Submodule (프로젝트 내 포함)
   - 장점: 최고의 자동화
   - 단점: 저장소 크기 +300-500MB, 초기 복제 5-10분
   ❌ 거절: 저장소 크기 제약 위반

2. CMakePresets.json만 (수동 vcpkg 설치)
   - 장점: 간단
   - 단점: 신규 개발자 수동 설정 필요
   ❌ 거절: 자동화 수준 부족

3. 하이브리드 (선택) ✅
   - 자동화 + 경량성 + 재현성의 균형
```

---

### 2. CMakePresets.json (플랫폼별 preset 분리)

**결정**:
```json
{
  "configurePresets": [
    {"name": "default", "hidden": true,
     "cacheVariables": {"CMAKE_TOOLCHAIN_FILE": "$env{VCPKG_ROOT}/..."}},
    {"name": "windows-x64", "inherits": "default", "generator": "Visual Studio 17"},
    {"name": "macos-x64", "inherits": "default", "cacheVariables": {"VCPKG_TARGET_TRIPLET": "x64-osx"}},
    {"name": "macos-arm64", "inherits": "default", "cacheVariables": {"VCPKG_TARGET_TRIPLET": "arm64-osx"}}
  ]
}
```

**근거**:
- ✅ CMake 3.23+ 표준 방식 (Microsoft 공식 가이드)
- ✅ IDE 네이티브 지원 (Visual Studio, VS Code, Xcode)
- ✅ CI/CD 자동화 용이 (`cmake --preset <name>`)
- ✅ 플랫폼별 전문화된 설정 가능

---

### 3. 플랫폼별 Triplet 선택

**결정**:
| 플랫폼 | Triplet | 이유 |
|--------|---------|------|
| Windows x64 | `x64-windows` | MSVC 2022 표준 |
| macOS Intel | `x64-osx` | Apple Silicon 이전 Mac |
| macOS ARM64 | `arm64-osx` | M1/M2/M3 칩 |

**근거**:
- ✅ vcpkg 공식 지원 triplet
- ✅ 각 플랫폼/아키텍처별 최적화
- ✅ 향후 Linux 추가 시에도 호환

---

### 4. 빌드 자동화 스크립트

**설계**:
```bash
# setup-dev.sh (macOS/Linux)
1. VCPKG_ROOT 기본값 설정 ($HOME/vcpkg)
2. vcpkg 존재 확인
   - 없으면: git clone + bootstrap
   - 있으면: 스킵
3. VCPKG_ROOT 환경 변수 설정
   - 현재 세션: export VCPKG_ROOT=...
   - 다음 세션: ~/.bashrc/~/.zshrc에 추가
4. 완료 메시지

# setup-dev.bat (Windows)
1. VCPKG_ROOT 기본값 설정 (C:\vcpkg)
2. vcpkg 존재 확인
   - 없으면: git clone + bootstrap
   - 있으면: 스킵
3. VCPKG_ROOT 환경 변수 설정 (setx로 영구 설정)
4. 완료 메시지
```

**장점**:
- ✅ 멱등성(Idempotent): 여러 번 실행해도 안전
- ✅ 자동 감지: 이미 설치된 vcpkg 재사용 가능
- ✅ 환경 변수 자동 설정 (다음 터미널부터 자동)

---

## 위험 / 트레이드오프

### 위험 1: Qt 6.5 첫 빌드 시간
**문제**: vcpkg에서 Qt 6.5를 처음 빌드할 때 **30-60분** 소요
```
첫 빌드: 30-60분 (Qt 컴파일)
이후: 5-10분 (캐시 사용)
```

**완화 방법**:
- ✅ BUILD.md에 "시간 소요 예상" 명시
- ✅ 백그라운드에서 실행 권고
- ✅ 바이너리 캐싱 활성화 (GitHub Actions 연동 시)

### 위험 2: 환경 변수 설정 확인 부족
**문제**: VCPKG_ROOT 미설정 시 CMake 오류 발생
```
CMake Error: CMAKE_TOOLCHAIN_FILE not found
```

**완화 방법**:
- ✅ setup-dev 스크립트가 명시적으로 설정
- ✅ DEVELOPMENT.md에 트러블슈팅 섹션 추가
- ✅ cmake 오류 메시지에 가이드 링크 추가

### 위험 3: macOS 아키텍처 혼동
**문제**: Intel Mac에서 `arm64-osx` triplet 사용 시 빌드 실패
```
cmake --preset macos-arm64  # 잘못된 선택 시 실패
```

**완화 방법**:
- ✅ BUILD.md에서 명확한 선택 가이드
- ✅ CMakePresets.json에 설명 주석 추가
- ✅ setup-dev.sh가 아키텍처 감지 (향후 개선)

### 위험 4: CI/CD 환경 변수 설정
**문제**: GitHub Actions에서 VCPKG_ROOT 설정 필요
```
workflow에 env: VCPKG_ROOT 추가 필요
```

**완화 방법**:
- ✅ CI/CD 변경은 별도로 진행 (이 변경 외 범위)
- ✅ setup-dev 스크립트가 기본값으로 호환성 제공

---

## 트레이드오프 분석

### 저장소 크기 vs 자동화 수준

| 방식 | 크기 | 자동화 | 선택 |
|------|------|--------|------|
| 1. CMakePresets.json만 | 0 | 40% | ❌ 불충분 |
| 2. Submodule 포함 | +500MB | 100% | ❌ 제약 위반 |
| 3. 하이브리드 (선택) | 0 | 90% | ✅ 최적 |

**선택 근거**: 80/20 규칙
- 90% 자동화를 0 추가 저장소로 달성
- 남은 10% (VCPKG_ROOT 환경변수 설정)은 스크립트가 자동 처리

---

## 마이그레이션 계획

### Phase A: 정보 수집 (1-2일)
1. baseline 최신 hash 확인
2. 대상 플랫폼 (Windows/macOS) 검증

### Phase B: 파일 생성 (2-3일)
1. CMakePresets.json 작성
2. vcpkg-configuration.json 작성
3. setup-dev.sh / setup-dev.bat 작성

### Phase C: 검증 (2-3일)
1. Windows에서 setup-dev.bat 및 빌드 검증
2. macOS Intel에서 setup-dev.sh 및 빌드 검증
3. macOS ARM64 (M1/M2) 검증 (가능시)

### Phase D: 문서화 (1-2일)
1. BUILD.md 작성 (크로스 플랫폼 가이드)
2. DEVELOPMENT.md 작성 (온보딩 가이드)

### Phase E: 최종 검증 (1일)
1. openspec validate 성공 확인
2. 모든 개발자가 setup-dev 스크립트 실행 가능 확인

**총 소요 시간**: 약 1-2주 (병렬 진행 가능)

---

## 열린 질문

1. **macOS 아키텍처 자동 감지**: setup-dev.sh가 `arm64-osx` vs `x64-osx` 자동 선택?
   - 현재: 수동 선택 (cmake --preset macos-arm64)
   - 향후: 스크립트 개선으로 자동 감지 가능

2. **CI/CD 바이너리 캐싱**: vcpkg 바이너리 캐싱 활성화?
   - 현재: GitHub Actions 연동 미포함
   - 추천: `setup-cross-platform-ci` 변경으로 별도 진행

3. **Linux 지원**:언제부터 추가?
   - 현재: 로드맵 외
   - 추천: macOS/Windows 검증 후 `setup-linux-build` 변경

4. **IDE 설정 자동화**: VS Code/Visual Studio/Xcode 통합?
   - 현재: CMakePresets.json만 (네이티브 지원)
   - 추천: 필요시 별도 `.vscode/settings.json` 추가

