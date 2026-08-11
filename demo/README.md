# 쇼케이스 데모 패키지 (S7)

이 폴더를 **통째로 데모 노트북에 복사**하고 `index.html`을 브라우저로 열면 끝입니다.
인터넷·서버·GPU·LLM 모두 불필요 (OpenAlex 레코드 링크만 온라인일 때 열림).

| 파일 | 내용 |
|---|---|
| `index.html` | 7개 화면 랜딩 + 3분 핵심 동선과 심화 탐색 구분 |
| `demo_static.html` | 출처 초록의 지지 범위를 검토한 질의 3건 + 인용 칩 → 출처 카드 (`#q1`~`#q3` 딥링크) |
| `cluster_map.html` | 연구 테마 지도 (40 클러스터, UMAP 배치) — 휠/드래그로 확대·이동, 클러스터 클릭 시 이웃 강조 |
| `theme_alluvial.html` | 시기별 클러스터의 인용 연결 alluvial (리본 폭 = 인용 수) |
| `knowledge_sankey.html` | 5개 연속 시기 사이 직접 인용 Sankey (기본 인접 4개, 토글 시 전체 10개 시기쌍) |
| `knowledge_flow.html` | 표준가스 질의 조건부 13편·12개 직접 인용 + 노드별 제목·초록 검토 요약 |
| `research_timeline.html` | 같은 13편을 4개 연속 구간에 한 번씩 배치 + 구간별 검토 요약과 근거 레코드 |
| `flow_dossier.html` | 논문 클릭 → 한국어 검토 요약·범위 + OpenAlex 초록 + 관측된 부모·자식 인용 관계 |

## 발표 전 체크 (2분)

- [ ] `index.html`을 열어 7개 링크가 모두 열리는지 확인
- [ ] `demo_static.html`에서 인용 칩 하나 클릭 → 오른쪽 출처 카드 하이라이트 확인
- [ ] `knowledge_sankey.html` 기본 화면에 인접 리본 4개가 보이고, `전체 보기`에서 10개로 바뀌는지 확인
- [ ] Sankey 띠 hover 후 마우스를 떼면 강조가 풀리는지 확인
- [ ] 브라우저 확대: 답변 **125%**, 지도·연결 **100~110%** (뒷줄 가독성과 전체 구조를 함께 확인)
- [ ] 지도에서 휠 확대 · 클러스터 클릭 → 이웃 강조 동작 확인 (`전체` 버튼으로 복귀)
- [ ] 발표용 탭 3개(`cluster_map`, `demo_static`, `knowledge_sankey`)를 미리 열어두기

## 데모 순서 (3분)

1. **지도**(30초) — “KRISS 시드 문헌과 배경 문헌을 함께 놓은 탐색 지도입니다”
2. **답변**(90초) — 질의 1개와 인용 칩을 보여주고 검토 상태 3단계(ID PASS / 출처 지지 PASS / 전문가 NOT_RUN)를 읽기
3. **Sankey**(45초) — 선행 시기→후속 시기는 지식 흐름 방향이고 실제 인용 행위는 반대라고 먼저 설명
4. **마무리**(15초) — “코퍼스 전체에서 질의별 논문 계보까지 줌인할 수 있습니다”

`theme_alluvial.html`과 표준가스 focus 3종은 발표 본 동선에 넣지 않고 질의응답·체험용으로 둡니다.

## 한계 (미리 알고 답할 것)

- **자유 질의 불가**: 이 페이지는 사전 실행 결과를 구운 것. 임의 질문은 검색·생성 서버 필요
  (`make serve` + 로컬 LLM). 체험 코너를 운영할 때만 준비.
- 코퍼스는 KRISS 연구자 시드 7,970편과 배경 문헌 10,882편의 혼합이며, 현재 답변 검토는 OpenAlex 제목·초록 범위입니다.
- 인용 ID의 실재와 출처의 주장 지지는 다른 검사입니다. 공개 3건은 둘 다 통과했지만 측정·화학 분야 전문가 검토는 `NOT_RUN`입니다.
- Sankey·alluvial의 띠는 직접 인용 횟수이며 영향력·인과·테마 변환을 뜻하지 않습니다.
- 논문 흐름·타임라인·dossier는 전체 코퍼스 결론이 아니라 표준가스 질의 조건부 13편 서브그래프입니다.
- 세 화면의 한국어 내용은 로컬 OpenAlex 제목·초록의 지지 범위를 검토한 결과(`PASS`)이며,
  인용 연결은 내용상 계승·영향력·동의·인과를 뜻하지 않습니다. 측정·화학 분야 전문가 검토는 `NOT_RUN`입니다.
- 제외한 5건의 상태와 사유는 원본 저장소 `experiments/kriss_chem_demo/review_manifest.json`에 보존합니다.

## 원본·재생성

원본 저장소: `~/Desktop/Workspace/1.4.1.2.CiteSage-KRISS` (브랜치 `kriss-chem`)

```bash
# 질의 추가/교체 (한국어는 토큰 2배 → MAX_TOKENS 필수)
SCISCI_MAX_TOKENS=4000 uv run python scisci/ask.py "질문" > experiments/kriss_chem_demo/demo_qN.out
# review_manifest.json에서 선별·출처지지 PASS 후 실행
# (빌더는 잘린 답변, 미검토 답변, 미사용 출처 카드, 코퍼스에 없는 인용을 거부함)
uv run python experiments/kriss_chem_demo/build_static_demo.py
# 코퍼스 전체 시각화
uv run python scisci/build_clusters.py && uv run python scisci/build_cluster_layout.py \
  && uv run python scisci/build_cluster_artifact.py
# Sankey + 표준가스 focus 3종
uv run python scisci/build_sankey_artifact.py
# 13편 라벨·요약·범위와 4개 구간 요약은 data/viz/kriss_focus_content.json에서 관리
uv run python scisci/build_flow_graph.py "중량법 표준가스 조제 불확도 흡착 안정성" -o disruption_flow.json --seeds 8
uv run python scisci/build_timeline.py disruption_flow.json -o disruption_timeline.json
uv run python scisci/build_dossiers.py
uv run python scisci/build_flow_artifact.py && uv run python scisci/build_timeline_artifact.py \
  && uv run python scisci/build_flow_dossier_artifact.py
```

슬라이드 삽입용 PNG 캡처는 원본 저장소의 `artifacts/captures/`에 있습니다.
설계 결정·실패 기록은 같은 저장소 `docs/JOURNEY.md`(Phase 9)와 `docs/LESSONS.md`.
