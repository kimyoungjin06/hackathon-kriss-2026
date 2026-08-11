# 출처와 검증 범위

이 문서는 공개 자료에 사용한 근거를 주장·데이터·시각화 단위로 기록합니다. 내부 서신과 운영 기록은 출처로 공개하지 않습니다.

## 상태 표기

| 상태 | 의미 |
|---|---|
| `SOURCE_VERIFIED` | 공식 원문 또는 공식 API에서 출처와 내용을 확인함 |
| `DERIVED` | 공개 원자료에서 코드로 계산하거나 변환함 |
| `EVENT_CONFIG` | 이 행사에 맞게 정한 시간·팀·발표 구성 |
| `EXPERT_REVIEW_NOT_RUN` | 식별자와 출처 범위는 확인했지만 분야 전문가 검토는 하지 않음 |

## 행사 구성

| 내용 | 상태 | 범위 |
|---|---|---|
| 30분 강의, 10분 팀 구성, 100분 해킹, 40분 발표 | `EVENT_CONFIG` | 2026년 KRISS 화학소재측정본부 워크숍용 구성 |
| 12팀 × 1분, 투표, 상위 4팀 × 4분 | `EVENT_CONFIG` | 다른 행사에 그대로 적용되는 표준이 아님 |

## 교육 사례

| 자료 | 사용 범위 |
|---|---|
| [LLM Hackathon for Applications in Materials Science and Chemistry](https://llmhackathon.github.io/) | 화학·재료 분야 해커톤 맥락 |
| [2024 hackathon retrospective, arXiv:2411.15221](https://arxiv.org/abs/2411.15221) | 2024년 운영과 사례 |
| [34 examples, arXiv:2505.03049](https://arxiv.org/abs/2505.03049) | 프로젝트 유형과 사례 |
| [2025 Agentic AI for Science collection, arXiv:2605.03205](https://arxiv.org/abs/2605.03205) | 에이전트형 과학 워크플로 사례 |
| [Agentic AI for Science Hackathon](https://iopscience.iop.org/article/10.1088/2632-2153/ae7f6a) | 과학 해커톤 스캐폴딩 사례 |
| [교육용 바이브코딩 해커톤, arXiv:2604.22747](https://arxiv.org/abs/2604.22747) | 짧은 교육형 해커톤 구성 참고 |

프로젝트별 성능 수치는 원문 조건과 평가 방법을 함께 읽지 않으면 비교할 수 없습니다. 이 저장소는 위 논문들의 결과를 독립 재현했다고 주장하지 않습니다.

## 데이터

### UCI 가스센서 드리프트

- 공식 데이터: [Gas Sensor Array Drift Dataset](https://archive.ics.uci.edu/dataset/224/gas)
- DOI: [10.24432/C5RP6W](https://doi.org/10.24432/C5RP6W)
- 공식 라이선스 표기: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 공개본: `data/gas_sensor_drift.csv`
- 처리: 원본 128개 특징 중 센서별 정상상태 특징 2개를 선택하고 배치·가스 라벨을 추가함
- 상태: `SOURCE_VERIFIED`, `DERIVED`
- 확인일: 2026-08-12

### BIPM KCDB

- 공식 서비스: [BIPM KCDB](https://www.bipm.org/kcdb/)
- 공식 API 안내: [API KCDB](https://www.bipm.org/en/cipm-mra/kcdb-api)
- 공개본: `data/kcdb_kriss_cmc.csv`, `data/kcdb_kriss_cmc_snapshot.json`
- 수집 범위: 화학·생물 분야에서 국가 코드 `KR`로 반환된 CMC 428건
- 스냅샷 기준일: 2026-08-06
- 상태: `SOURCE_VERIFIED`, `DERIVED`
- 주의: API가 공개되어 있다는 사실과 원자료 전체에 별도 오픈 라이선스가 부여됐다는 주장은 구분합니다. BIPM 출처를 유지하고 최신 값은 공식 서비스에서 확인해야 합니다.

## CiteSage 쇼케이스

- 메타데이터·인용 관계: [OpenAlex](https://openalex.org/)
- OpenAlex 데이터 조건: [CC0](https://help.openalex.org/access/pricing/#free-data-paid-services)
- 화면의 `W...` 식별자는 OpenAlex Work ID입니다.
- 시각화는 OpenAlex 메타데이터와 인용 연결을 가공한 `DERIVED` 결과입니다.
- 인용 ID의 존재와 출처 초록의 주장 범위는 공개 질의에 대해 점검했습니다.
- 측정·화학 분야 전문가 검토 상태는 `EXPERT_REVIEW_NOT_RUN`입니다.

인용 연결은 두 문헌 사이에 인용 관계가 있음을 뜻할 뿐, 내용상 계승·동의·인과 또는 품질을 보장하지 않습니다. 논문 전문은 이 저장소에 포함하지 않습니다.
