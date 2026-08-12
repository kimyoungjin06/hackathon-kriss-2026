#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_dir"

build_doc() {
  local source_file="$1"
  local output_dir="$2"
  local title="$3"
  local code="$4"
  local state="$5"
  local description="$6"

  mkdir -p "$output_dir"
  pandoc "$source_file" \
    --from=gfm \
    --to=html5 \
    --standalone \
    --toc \
    --toc-depth=2 \
    --template=templates/public-doc.html \
    --lua-filter=scripts/public-links.lua \
    --metadata "title=$title" \
    --metadata "doc-code=$code" \
    --metadata "page-route=$output_dir" \
    --metadata "page-state=$state" \
    --metadata "page-description=$description" \
    --output "$output_dir/index.html"
}

build_doc PROGRAM.md program "공개 프로그램" "PROGRAM" "임시 자료" "180분 동안 강의, 실습과 발표를 진행하는 전체 흐름을 확인합니다."
build_doc API_GUIDE.md api "API 안내" "API GUIDE" "공개 초안" "공개·합성 데이터로 API 실습을 시작할 때 필요한 연결 형식과 안전 원칙입니다."
build_doc PARTICIPANT_GUIDE.md guide "참가자 안내" "GUIDE" "공개" "준비물, 팀 역할, 과제 트랙과 제출물을 한 번에 확인합니다."
build_doc EXAMPLES.md examples "3시간 산출물 예시" "EXAMPLES" "공개" "해커톤 시간 안에 만들 수 있는 네 가지 현실적인 결과물과 완성 기준입니다."
build_doc SOURCES.md sources "출처와 검증 범위" "SOURCES" "공개" "공개 자료의 근거와 상태를 주장, 데이터와 시각화 단위로 기록합니다."
build_doc RIGHTS_AND_ATTRIBUTION.md rights "권리와 출처 표시" "RIGHTS" "공개" "저장소 작성물과 제3자 데이터·메타데이터의 권리와 출처 조건을 구분합니다."

printf 'Built 6 public document pages.\n'
