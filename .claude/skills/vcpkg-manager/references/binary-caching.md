# vcpkg 바이너리 캐싱 레퍼런스

바이너리 캐싱은 빌드된 패키지를 저장하여 다른 머신이나 CI에서 재컴파일을 방지합니다.

## 캐시 제공자

### 로컬 파일시스템 (기본값)
```bash
# 기본 위치
# Linux/macOS: ~/.cache/vcpkg/archives
# Windows: %LOCALAPPDATA%\vcpkg\archives

# 커스텀 경로
export VCPKG_BINARY_SOURCES="clear;files,/path/to/cache,readwrite"
```

### NuGet (Azure Artifacts, GitHub Packages)
```bash
# Azure DevOps
export VCPKG_BINARY_SOURCES="clear;nuget,https://pkgs.dev.azure.com/ORG/PROJECT/_packaging/FEED/nuget/v3/index.json,readwrite"

# GitHub Packages
export VCPKG_BINARY_SOURCES="clear;nuget,https://nuget.pkg.github.com/OWNER/index.json,readwrite"
```

### AWS S3
```bash
export VCPKG_BINARY_SOURCES="clear;x-aws,s3://bucket-name/cache-prefix/,readwrite"
```

### Google Cloud Storage
```bash
export VCPKG_BINARY_SOURCES="clear;x-gcs,gs://bucket-name/cache-prefix/,readwrite"
```

### Azure Blob Storage
```bash
export VCPKG_BINARY_SOURCES="clear;x-azblob,https://account.blob.core.windows.net/container,readwrite"
```

### GitHub Actions 캐시
```bash
export VCPKG_BINARY_SOURCES="clear;x-gha,readwrite"
export ACTIONS_CACHE_URL="..."  # GitHub Actions에서 자동 제공
export ACTIONS_RUNTIME_TOKEN="..."  # GitHub Actions에서 자동 제공
```

## 접근 모드

| 모드 | 설명 |
|------|------|
| `read` | 다운로드만 |
| `write` | 업로드만 |
| `readwrite` | 다운로드 및 업로드 |

## 여러 소스 사용 (폴백 체인)
```bash
# 원격 먼저 시도, 로컬로 폴백
export VCPKG_BINARY_SOURCES="clear;nuget,https://remote/feed,read;files,/local/cache,readwrite"
```

## CI 설정 예시

### GitHub Actions
```yaml
- name: Setup vcpkg
  uses: lukka/run-vcpkg@v11
  with:
    vcpkgGitCommitId: 'a0e1a0e7c6eb6e6c1ca82502c3ad3bb6c8a63dd5'
  env:
    VCPKG_BINARY_SOURCES: "clear;x-gha,readwrite"
```

### GitLab CI
```yaml
variables:
  VCPKG_BINARY_SOURCES: "clear;files,${CI_PROJECT_DIR}/.vcpkg-cache,readwrite"
cache:
  paths:
    - .vcpkg-cache/
```

### Azure Pipelines
```yaml
variables:
  VCPKG_BINARY_SOURCES: 'clear;nuget,$(VCPKG_NUGET_FEED),readwrite'
```

## 환경변수

| 변수 | 설명 |
|------|------|
| `VCPKG_BINARY_SOURCES` | 캐시 설정 |
| `VCPKG_NUGET_REPOSITORY` | NuGet 소스 URL |
| `VCPKG_KEEP_ENV_VARS` | 빌드 중 환경변수 유지 |
| `X_VCPKG_ASSET_SOURCES` | 에셋 캐싱 (다운로드) |

## 문제 해결

```bash
# 캐시 설정 확인
vcpkg install fmt --debug

# 로컬 캐시 삭제
rm -rf ~/.cache/vcpkg/archives/*

# 캐시 무시하고 강제 빌드
vcpkg install fmt --no-binarycaching
```
