# KRISS 화학소재측정본부 AI 해커톤

KRISS 화학소재측정본부 워크숍을 위해 만든 3시간 AI 해커톤 교육 패키지입니다. 참가자가 생성형 AI를 이용해 작은 업무 도구를 만들고, 결과의 근거와 한계를 직접 검증하는 과정을 지원합니다.

이 저장소는 교육·행사 진행용 자료입니다. KRISS의 정책, 측정표준 또는 측정능력에 대한 공식 해석을 제공하지 않습니다.

## 바로 시작하기

- [공개 자료 대문](https://kimyoungjin06.github.io/hackathon-kriss-2026/) — 프로그램, CiteSage와 행사용 API 안내로 이동
- [행사 허브](https://kimyoungjin06.github.io/hackathon-kriss-2026/event-hub/) — 일정, 트랙, 데이터 규칙과 제출물
- [CiteSage 쇼케이스](https://kimyoungjin06.github.io/hackathon-kriss-2026/demo/) — 오프라인으로 열리는 연구 문헌 탐색 데모
- [API 안내](https://kimyoungjin06.github.io/hackathon-kriss-2026/api/) — 공개 가능한 연결 범위와 데이터 안전 원칙
- [참가자 안내](https://kimyoungjin06.github.io/hackathon-kriss-2026/guide/) — 준비물, 역할, 진행 규칙
- [공개 프로그램](https://kimyoungjin06.github.io/hackathon-kriss-2026/program/) — 180분 구성과 학습 목표
- [산출물 예시](https://kimyoungjin06.github.io/hackathon-kriss-2026/examples/) — 3시간 안에 만들 수 있는 네 가지 결과물

정적 페이지는 별도 서버나 설치 없이 브라우저에서 열 수 있습니다.

## 180분 프로그램

| 구간 | 내용 |
|---|---|
| 0:00–0:30 | 강의, 라이브 데모, 화학·재료 분야 사례 |
| 0:30–0:40 | 팀별 과제 선택과 목표 선언 |
| 0:40–2:20 | 100분 해킹 |
| 2:20–3:00 | 12팀 × 1분 발표, 현장 투표, 상위 4팀 × 4분 발표 |

## 공개 구성

| 경로 | 내용 |
|---|---|
| `index.html` | 프로그램·CiteSage·행사용 API 안내를 연결하는 공개 대문 |
| `event-hub/` | 행사 진행용 첫 화면 |
| `demo/` | CiteSage 정적 쇼케이스 7개 화면 |
| `data/` | UCI 가스센서 드리프트와 BIPM KCDB 교육용 데이터 |
| `program/`, `api/`, `guide/` | 프로그램·API·참가자 안내 웹 문서 |
| `examples/`, `sources/`, `rights/` | 예시·출처·권리 안내 웹 문서 |
| `*.md` | 웹 문서의 원본 Markdown |
| `scripts/build_public_docs.sh` | Markdown에서 공개 웹 문서를 다시 만드는 스크립트 |

운영 인력, 연락망, 계정·키 배포, 비용, 서신과 준비 일정은 이 공개 저장소에 포함하지 않습니다.

## 데이터 안전 원칙

- 공개 자료와 교육용·합성 데이터만 사용합니다.
- 개인정보, 인증정보, 계약·보안 정보는 외부 AI에 입력하지 않습니다.
- 내부 구조를 반영한 데이터는 비식별화만으로 충분한지 먼저 판단하고, 애매하면 합성 데이터로 대체합니다.
- AI가 만든 수치·인용·분류 결과는 원문이나 코드로 다시 확인합니다.

## 근거와 한계

데이터와 주요 사례의 출처는 [출처와 검증 범위](https://kimyoungjin06.github.io/hackathon-kriss-2026/sources/)에 기록합니다. CiteSage 화면의 연결은 OpenAlex의 문헌 메타데이터와 인용 관계를 시각화한 것으로, 내용상 계승·동의·인과관계나 영향력을 직접 의미하지 않습니다. 측정·화학 분야 전문가 검토가 완료되지 않은 결과는 교육용 탐색 결과로만 사용해야 합니다.

재사용 전에 [권리와 출처 표시](https://kimyoungjin06.github.io/hackathon-kriss-2026/rights/)를 확인해 주세요. 저장소 전체에 단일 라이선스를 적용하지 않으며, 원본 데이터와 제3자 메타데이터에는 각각의 조건이 적용됩니다.
