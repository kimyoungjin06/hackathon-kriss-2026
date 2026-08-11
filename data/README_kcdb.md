# 트랙 B 실습 데이터 — KRISS 국제 인정 측정능력(CMC) · BIPM KCDB

## 파일

| 파일 | 내용 |
|---|---|
| `kcdb_kriss_cmc.csv` | KRISS 화학·생물 CMC **428건** × 18열 · 84KB · 엑셀로 바로 열림 |
| `kcdb_kriss_cmc_snapshot.json` | 같은 428건의 API 원본(전 필드) — 오프라인 백업 |
| `pull_kcdb.py` | 최신 데이터 재수집 스크립트 (아래 API 사용법 참조) |

## 왜 이 데이터인가

- **자기 기관 데이터입니다.** KRISS가 CIPM MRA 아래 국제적으로 인정받은 측정능력 목록.
- **정답이 공개돼 있습니다.** 모든 레코드에 `kcdbCode`(예: `APMP-QM-KR-000000IH-1`)가 있어
  [KCDB 웹사이트](https://www.bipm.org/kcdb/)에서 그대로 조회·대조됩니다 →
  **화학 도메인 지식 없이도 결과 검증이 가능**합니다(멘토·심사에 결정적).
- **API가 열려 있습니다.** 인증키 불필요. 그래서 산출물이 "대화"가 아니라 **파이프라인**이 됩니다.

**KRISS 428건 구성**: 가스 176 · 식품 136 · 첨단소재 38 · 무기용액 35 · 생체시료 22 · 유기용액 9

## 컬럼 (CSV)

| 컬럼 | 의미 |
|---|---|
| `kcdbCode` | KCDB 고유 코드 (웹사이트 대조용) |
| `categoryValue` / `subCategoryValue` | 분류 (가스/식품/첨단소재 …) |
| `analyteValue` / `analyteMatrix` | 분석종 / 매트릭스 (예: mercury / ABS) |
| `quantityValue` | 측정량 (Mass fraction 등) |
| `cmc_low` · `cmc_high` · `cmc_unit` | 인정 측정범위 |
| `unc_low` · `unc_high` · `unc_unit` | 확장불확도 범위 |
| `uncertaintyMode` | Relative(398건) / Absolute(30건) — **혼재 주의** |
| `coverageFactor` · `confidenceLevel` | 포함인자(k) · 신뢰수준 |
| `mechanism` | 근거 CRM 번호 등 |
| `publicationDate` · `status` | 등록일 · 상태 |

---

## 실제로 돌려본 예시 4개 (멘토용 정답지)

아래는 **이 데이터로 미리 실행해 확인한 결과**입니다. 팀이 도달할 수 있는 지점이자,
멘토가 결과의 타당성을 즉석에서 판정하는 기준입니다.

### 예시 A — 공백 분석: 남들은 있고 우리는 없는 것

가스 분야 전 세계 CMC 2,041건(28개국)을 분석종 기준으로 비교하면:
**전 세계 175종 중 KRISS 보유 81종.** 3개 기관 이상이 보유하는데 KRISS에는 없는 상위 항목:

| 보유 기관 수 | 분석종 |
|---|---|
| 16 | n-pentane |
| 11 | n-hexane |
| 10 | neo-pentane, isobutane |
| 7 | i-pentane |
| 5–6 | 1-butene, sulphur dioxide, hexane, airborne particles |

→ **신규 CMC 후보 도출**이라는 실제 기관 기획 업무가 됩니다.

### 예시 B — 불확도 벤치마킹: 우리는 어디쯤인가

같은 분석종·매트릭스에서 KRISS와 타국의 상대불확도 상한을 비교하면 (낮을수록 우수):

| 분석종 / 매트릭스 | KRISS | 타국 최저 | 비교 기관 수 |
|---|---|---|---|
| oxygen / nitrogen | **0.02 %** | 0.08 % | 52 |
| nitrogen / helium | **0.20 %** | 1.00 % | 5 |
| nitrogen dioxide / nitrogen | 3.00 % | **0.30 %** | 6 |
| hydrogen / nitrogen | 1.00 % | **0.12 %** | 10 |
| methane / nitrogen | 0.30 % | **0.05 %** | 24 |

> ⚠️ **이 표는 함정입니다 — 그래서 좋은 과제입니다.** 기관마다 인정 *측정범위*가 다르고
> 매트릭스가 같아도 농도 구간·측정법이 다를 수 있습니다. "불확도 상한이 낮다 = 더 우수하다"로
> 단정하면 틀립니다. **AI는 이 표를 자신 있게 만들어 주고, 단서는 붙이지 않습니다.**
> 이 함정을 잡아내는 것이 팀 판정관(시니어 연구자)의 역할이고, 이 실습의 핵심입니다.

### 예시 C — 등록 노후도

KRISS 428건 중 **2015년 이전 등록이 133건(31%)**. 가장 오래된 것은 **2001-10-21**에 등록된
생체시료(사람 혈청) 중 creatinine·urea·uric acid 항목들입니다.

→ "갱신 검토 대상 목록" 자동 생성 도구가 나옵니다.

### 예시 D — CMC ↔ CRM 연결 상태

`mechanism` 필드는 428건 전부에 값이 있고, 그중 **CRM 번호가 명시된 것은 366건**
(예: magnesium → `CRM 105-02-017`). **62건은 CRM 번호가 없습니다.**

→ 연결 누락인지 원래 CRM 기반이 아닌 항목인지 확인하는 **정합성 점검 도구**가 됩니다.

---

## 시작 프롬프트

1. *"이 CSV는 우리 기관이 국제적으로 인정받은 측정능력 목록이야. 카테고리별 보유 현황과
   불확도 분포를 요약하고, 등록일이 오래된 항목을 표로 뽑아줘."*
2. *"KCDB 공개 API로 특정 분석종을 전 세계 기관 기준으로 받아와서, 우리 기관과 같은
   분석종·매트릭스를 가진 다른 기관들의 불확도를 비교하는 표를 만들어줘."*
3. *"우리가 보유하지 않은 분석종 중 여러 기관이 이미 인정받은 것을 찾아 신규 후보 목록을
   만들어줘. 몇 개 기관이 보유했는지도 함께."*
4. (반증 과제) *"방금 만든 불확도 비교표가 공정한 비교인지 검증해줘 — 측정범위·농도구간·
   측정법이 다를 수 있는데, 그걸 무시하면 어떤 오해가 생기는지 데이터로 보여줘."*

## API 사용법 (도구를 만들 팀용)

인증키 불필요. OpenAPI 명세: `https://www.bipm.org/api/kcdb/v3/api-docs`

```bash
curl -X POST https://www.bipm.org/api/kcdb/cmc/searchData/chemistryAndBiology \
  -H "Content-Type: application/json" \
  -d '{"metrologyAreaLabel":"QM","page":0,"pageSize":20,"showTable":true,"countries":["KR"]}'
```

- 필수 필드: `metrologyAreaLabel`(화학은 `QM`), `page`, `pageSize`, `showTable`
- 선택: `countries`(예 `["KR","JP"]`), `analyteLabel`, `categoryLabel`(가스=`4`, 식품=`11`), `keywords`
- 참조 데이터: `GET /api/kcdb/referenceData/{category|analyte|country|quantity}`
- 물리 분야는 `/cmc/searchData/physics`, 방사선은 `/radiation`

## 주의점

- **불확도 표기가 혼재**합니다: Relative 398건 / Absolute 30건, 단위는 %(407) · mg/kg(19) · nmol/mol(2).
  단위를 무시하고 숫자만 비교하면 틀립니다.
- 기관 간 비교 시 **측정범위(`cmc_low`~`cmc_high`)를 함께 보지 않으면 무의미**합니다(예시 B 경고 참조).
- 이 스냅샷은 2026-08-06 수집분입니다. KCDB는 갱신되므로 최신성이 중요하면 API를 직접 호출하세요.

## 출처

BIPM KCDB (Key Comparison Database), CIPM MRA. https://www.bipm.org/kcdb/
API 문서: https://www.bipm.org/en/cipm-mra/kcdb-api
