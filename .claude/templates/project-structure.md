# C++/QML Project Structure Template

## Standard Directory Layout

```
{project-name}/
├── .claude/                     # AI 에이전트 설정
│   ├── agents/                  # 에이전트 정의 (*.md)
│   ├── skills/                  # 스킬 정의
│   ├── templates/               # 프로젝트 템플릿
│   ├── orchestrator/            # Python 오케스트레이터
│   ├── workflow.json            # 워크플로우 규칙
│   └── session-state.json       # 세션 상태
│
├── external/                    # 외부 의존성
│   └── vcpkg/                   # vcpkg 서브모듈 (고정 경로)
│
├── openspec/                    # OpenSpec 명세
│   ├── project.md               # 프로젝트 컨벤션
│   ├── AGENTS.md                # AI 에이전트 지침
│   ├── specs/                   # 현재 스펙 (구축된 것)
│   │   └── {capability}/
│   │       ├── spec.md
│   │       └── design.md
│   └── changes/                 # 변경 제안
│       └── {change-name}/
│           ├── proposal.md
│           ├── tasks.md
│           └── specs/           # 델타 변경
│
├── src/                         # C++ 소스
│   ├── main.cpp                 # 앱 진입점
│   ├── app/                     # 애플리케이션 로직
│   │   ├── Application.cpp
│   │   └── Application.h
│   ├── models/                  # 데이터 모델
│   ├── services/                # 비즈니스 로직
│   └── utils/                   # 유틸리티
│
├── qml/                         # QML UI 파일
│   ├── Main.qml                 # 메인 윈도우
│   ├── components/              # 재사용 컴포넌트
│   ├── pages/                   # 페이지 뷰
│   └── qml.qrc                  # 리소스 파일
│
├── tests/                       # 테스트
│   ├── unit/                    # 단위 테스트
│   └── integration/             # 통합 테스트
│
├── docs/                        # 문서 (선택)
│
├── build/                       # 빌드 출력 (gitignore)
│   ├── windows-debug/           # 프리셋별 빌드 디렉토리
│   ├── windows-release/
│   ├── linux-debug/
│   ├── linux-release/
│   ├── macos-debug/
│   └── macos-release/
│
├── .github/                     # GitHub 설정
│   └── workflows/               # CI/CD 워크플로우
│
├── CMakeLists.txt               # 루트 CMake 설정
├── CMakePresets.json            # CMake 프리셋 (6개)
├── vcpkg.json                   # vcpkg 의존성
├── .gitignore                   # Git 무시 패턴
└── CLAUDE.md                    # Claude Code 지침
```

## Naming Conventions

### C++ Files
| 유형 | 패턴 | 예시 |
|------|------|------|
| 클래스 파일 | `PascalCase.cpp/h` | `UserService.cpp` |
| 헤더 가드 | `{PROJECT}_{PATH}_{FILE}_H` | `MYAPP_SERVICES_USERSERVICE_H` |
| 네임스페이스 | `snake_case` | `my_app::services` |

### QML Files
| 유형 | 패턴 | 예시 |
|------|------|------|
| 컴포넌트 | `PascalCase.qml` | `LoginForm.qml` |
| 페이지 | `{Name}Page.qml` | `HomePage.qml` |
| 뷰 | `{Name}View.qml` | `ProductListView.qml` |

### Build Output
- **규칙**: `build/${presetName}/`
- **실행 파일**: `build/${presetName}/bin/${target}`
- **라이브러리**: `build/${presetName}/lib/`

## Required Files

### 최소 필수 파일
```
CMakeLists.txt          # 빌드 설정
CMakePresets.json       # 6개 프리셋 (3 플랫폼 × 2 구성)
vcpkg.json              # 의존성 목록
.gitignore              # 표준 무시 패턴
CLAUDE.md               # AI 지침 (openspec/ 참조)
```

### OpenSpec 필수 파일
```
openspec/project.md     # 프로젝트 컨벤션
openspec/AGENTS.md      # AI 에이전트 지침
```

## CMakePresets Template

6개 표준 프리셋:
1. `windows-debug` - Windows Debug
2. `windows-release` - Windows Release
3. `linux-debug` - Linux Debug
4. `linux-release` - Linux Release
5. `macos-debug` - macOS Debug
6. `macos-release` - macOS Release

각 프리셋의 binaryDir: `${sourceDir}/build/${presetName}`

## vcpkg Integration

```bash
# 서브모듈 초기화
git submodule add https://github.com/microsoft/vcpkg.git external/vcpkg
git submodule update --init --recursive

# Bootstrap
./external/vcpkg/bootstrap-vcpkg.sh  # Linux/macOS
./external/vcpkg/bootstrap-vcpkg.bat  # Windows
```

## Scaffolding Checklist

새 프로젝트 생성 시:
- [ ] 디렉토리 구조 생성
- [ ] CMakeLists.txt 생성
- [ ] CMakePresets.json 생성 (6 프리셋)
- [ ] vcpkg.json 생성
- [ ] .gitignore 생성
- [ ] CLAUDE.md 생성
- [ ] openspec/ 초기화
- [ ] .claude/ 디렉토리 복사
- [ ] vcpkg 서브모듈 추가
- [ ] 초기 빌드 테스트
