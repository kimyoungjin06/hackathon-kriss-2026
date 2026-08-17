# CiteSage 정적 쇼케이스

KRISS 관련 문헌 코퍼스를 탐색하는 CiteSage 화면을 오프라인 정적 HTML로 구성한 교육용 데모입니다. 서버, GPU 또는 LLM 실행 없이 브라우저에서 열 수 있습니다.

## 실행

`index.html`을 브라우저로 열고 원하는 화면을 선택합니다.

| 화면 | 내용 |
|---|---|
| `cluster_map.html` | 연구 테마 지도 |
| `demo_static.html` | 인용 식별자와 출처 카드를 포함한 답변 예시 |
| `knowledge_sankey.html` | 시기 간 인용 연결 요약 |
| `theme_alluvial.html` | 연구 테마의 시기별 연결 |
| `knowledge_flow.html` | 선택 문헌의 인용 네트워크 |
| `research_timeline.html` | 선택 문헌의 시간 순서 |
| `flow_dossier.html` | 문헌별 선행·후속 관계 검토 화면 |

## 권장 시연 순서

1. `cluster_map.html`에서 코퍼스의 큰 연구 테마를 살펴봅니다.
2. `demo_static.html`에서 답변과 OpenAlex Work ID, 출처 카드를 함께 확인합니다.
3. `knowledge_sankey.html`에서 시기 간 연결을 살펴봅니다.

## 검증 범위

- 화면의 `W...` 값은 OpenAlex Work ID입니다.
- 공개 질의의 인용 ID 존재 여부와 출처 초록의 주장 범위를 확인했습니다.
- 측정·화학 분야 전문가 검토는 수행하지 않았습니다.
- 화면에 표시된 연결은 인용 관계이며 내용상 계승·동의·인과 또는 품질을 뜻하지 않습니다.
- Sankey 띠의 폭은 화면에 포함된 연결 수를 나타내며 연구 영향력의 직접 척도가 아닙니다.

이 저장소에는 원본 코퍼스와 전체 분석 파이프라인을 포함하지 않습니다. 다만
`bundle-manifest.json`은 각 공개 파일의 해시와 정본 Git 커밋, HTML 빌더 및 추적 입력 JSON의
해시를 기록합니다. CI는 manifest 불일치, 정본 export drift와 허용 목록 밖 오래된 파일을 거부합니다.
분석 데이터의 clean rebuild와 추적 JSON에서 HTML을 다시 그리는 public render는 서로 다른
검증 단계입니다.

메타데이터와 권리 정보는 [출처 대장](../SOURCES.md)과 [권리 고지](../RIGHTS_AND_ATTRIBUTION.md)를 참고하세요.
