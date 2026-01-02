# 구현 계획: Windows 빌드 환경 구축

## 1. 사전 검증
- [ ] 1.1 Visual Studio 2022 (MSVC) 설치 확인
- [ ] 1.2 CMake 4.2.0 이상 설치 확인
- [ ] 1.3 Git 설치 확인

## 2. vcpkg 설치 및 부트스트랩
- [ ] 2.1 `C:\vcpkg` 디렉토리에 vcpkg 저장소 클론
  ```bash
  git clone https://github.com/Microsoft/vcpkg.git C:\vcpkg
  ```
- [ ] 2.2 vcpkg 부트스트랩 실행
  ```bash
  cd C:\vcpkg
  .\bootstrap-vcpkg.bat
  ```
- [ ] 2.3 vcpkg 설치 확인
  ```bash
  vcpkg --version
  ```

## 3. CMake 빌드 설정
- [ ] 3.1 이전 빌드 캐시 제거
  ```bash
  cd C:\Dev\ai-supported-desktop-sw\toss-pos
  rm -rf build
  mkdir build
  ```
- [ ] 3.2 CMake 프로젝트 설정 (vcpkg 통합)
  ```bash
  cmake -S . -B build `
    -DCMAKE_TOOLCHAIN_FILE=C:\vcpkg\scripts\buildsystems\vcpkg.cmake `
    -DVCPKG_TARGET_TRIPLET=x64-windows
  ```
- [ ] 3.3 CMake 설정 검증 (에러 없음 확인)

## 4. 빌드 실행
- [ ] 4.1 Release 모드 빌드
  ```bash
  cmake --build build --config Release
  ```
- [ ] 4.2 빌드 결과 검증 (toss-pos.exe 생성 확인)
  ```bash
  dir build\Release\
  ```
- [ ] 4.3 Debug 모드 빌드 (선택사항)
  ```bash
  cmake --build build --config Debug
  ```

## 5. 애플리케이션 실행 테스트
- [ ] 5.1 생성된 실행 파일 실행
  ```bash
  .\build\Release\toss-pos.exe
  ```
- [ ] 5.2 UI 렌더링 확인 (창 표시, 레이아웃 정상)
- [ ] 5.3 기본 상호작용 테스트 (버튼 클릭, 탭 네비게이션)

## 6. 빌드 스크립트 작성 (선택사항)
- [ ] 6.1 `build_windows.bat` 또는 `build_windows.ps1` 작성
- [ ] 6.2 스크립트에 자동화된 빌드 명령 통합
- [ ] 6.3 스크립트 테스트

## 7. 개발자 가이드 작성
- [ ] 7.1 `BUILD_WINDOWS.md` 문서 작성
  - 필수 설치 사항
  - 단계별 빌드 지침
  - 트러블슈팅 가이드
- [ ] 7.2 `openspec/specs/toss-pos/spec.md` 업데이트 (빌드 요구사항 명시)

## 8. CI/CD 통합 (향후)
- [ ] 8.1 GitHub Actions 워크플로우 검토 (Windows 빌드)
- [ ] 8.2 `.cmake/CMakePresets.json` 작성 (자동화, 선택사항)

## 9. 최종 검증
- [ ] 9.1 모든 빌드 캐시가 Windows 경로 기반인지 확인
- [ ] 9.2 크로스 플랫폼 호환성 (macOS에서도 여전히 빌드 가능한지 확인, 향후)
- [ ] 9.3 OpenSpec 스펙 업데이트 검증

