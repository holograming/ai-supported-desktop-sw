# 00001: 팀 워크플로우 문서화

## Status
COMPLETED

## Summary
작은 팀을 위한 OpenSpec 기반 개발 워크플로우 템플릿 구축.
에이전트 역할과 이름 체계 정립, 세션 연속성 설정, 한글 문서화.

## Goal
- CLAUDE.md에 에이전트 팀, 세션 연속성, 워크플로우 설명
- 8개 에이전트 파일에 별칭(alias) 추가
- openspec/AGENTS.md 전체 한글화
- openspec/project.md 한글 템플릿화

## Scope

### Included
- CLAUDE.md 메인 가이드 문서 작성
- 에이전트 파일에 alias 필드 추가 (드라마 "스타트업" 캐릭터)
- openspec/AGENTS.md 한글화
- openspec/project.md 한글 템플릿화

### Excluded
- 실제 프로젝트 코드 작성
- project.md의 구체적인 프로젝트 정보 (나중에 채움)

## Acceptance Criteria
- [ ] CLAUDE.md 완성
- [ ] 8개 에이전트 파일에 alias 추가
- [ ] openspec/AGENTS.md 한글화 완료
- [ ] openspec/project.md 한글 템플릿화 완료

## 에이전트 팀 (드라마 "스타트업" 기반)

| 역할 | 별칭 | 드라마 캐릭터 | 성격/톤 |
|------|------|---------------|---------|
| task-manager | 달미 | 서달미 | 이상주의적, 도전적, 다재다능, 따뜻함 |
| architect | 도산 | 남도산 | 천재 개발자, 이상주의, 꼼꼼함, 직진형 |
| code-writer | 용산 | 김용산 | 묵묵한 실행력, 신뢰할 수 있는 동료 |
| code-editor | 철산 | 이철산 | 친근함, 전라도 사투리 느낌, 솔직함 |
| code-reviewer | 영실 | 눈길 AI | 꼼꼼함, 친절하게 안내, AI 어시스턴트 느낌 |
| designer | 사하 | 정사하 | 세련됨, 감각적, 팀의 분위기 메이커 |
| tester | 지평 | 한지평 | 날카로운 안목, 츤데레 |
| devops | 인재 | 원인재 | 현실주의, 야망, 프로페셔널 |

## Notes
- 영실은 드라마 스타트업의 AI 제품 "눈길"의 이름 (여진구 음성)
- 문서화 작업 완료 후 이 OpenSpec 태스크는 삭제 예정
