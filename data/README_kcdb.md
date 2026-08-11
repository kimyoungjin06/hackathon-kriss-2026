# KRISS CMC 교육 데이터

BIPM Key Comparison Database(KCDB)의 공개 API에서 수집한 KRISS 화학·생물 분야 Calibration and Measurement Capabilities(CMC) 스냅샷입니다. 공개 측정능력의 구성, 등록 시기와 데이터 품질을 탐색하는 실습에 사용합니다.

## 파일

| 파일 | 내용 |
|---|---|
| `kcdb_kriss_cmc.csv` | 분석용으로 정리한 CMC 428건 |
| `kcdb_kriss_cmc_snapshot.json` | 같은 조회 결과의 API 응답 보존본 |
| `pull_kcdb.py` | 공식 API에서 최신 자료를 다시 수집하는 스크립트 |

스냅샷 기준일은 2026-08-06입니다. 현재 값은 공식 KCDB에서 다시 확인해야 합니다.

## 주요 열

| 열 | 의미 |
|---|---|
| `kcdbCode` | KCDB 식별 코드 |
| `categoryValue`, `subCategoryValue` | 분야와 하위 분류 |
| `analyteValue`, `analyteMatrix` | 분석종과 매트릭스 |
| `quantityValue` | 측정량 |
| `cmc_low`, `cmc_high`, `cmc_unit` | 인정 측정범위 |
| `unc_low`, `unc_high`, `unc_unit` | 확장불확도 범위 |
| `uncertaintyMode` | 상대 또는 절대 불확도 표기 |
| `publicationDate`, `status` | 등록일과 상태 |

## 시작 질문

1. 카테고리별 CMC 구성과 등록 시기를 요약할 수 있는가?
2. 특정 분석종·매트릭스의 측정범위와 불확도 표기를 비교할 수 있는가?
3. 오래된 등록 항목을 검토 후보로 정리할 수 있는가?
4. 다른 기관과 비교할 때 측정범위·단위·불확도 방식을 함께 확인했는가?

## 해석할 때 주의할 점

- 상대불확도와 절대불확도가 섞여 있습니다.
- 숫자가 작다는 사실만으로 더 우수한 측정능력이라고 결론내릴 수 없습니다.
- 분석종과 매트릭스가 같아도 측정범위, 농도 구간과 방법이 다를 수 있습니다.
- 등록일이 오래됐다는 사실만으로 CMC가 유효하지 않다고 판단할 수 없습니다.

## 출처

- [BIPM KCDB](https://www.bipm.org/kcdb/)
- [KCDB API 안내](https://www.bipm.org/en/cipm-mra/kcdb-api)

BIPM 출처와 스냅샷 날짜를 유지해야 합니다. 이 저장소는 공개 API 제공 사실을 넘어 원자료에 별도 오픈 라이선스가 적용된다고 주장하지 않습니다. 자세한 범위는 [출처 대장](../SOURCES.md)과 [권리 고지](../RIGHTS_AND_ATTRIBUTION.md)를 참고하세요.
