# ForWriter Citation Library Workflow

이 문서는 EPUB/PDF 원문을 바탕으로 책 설명, 주제 태그, 인용 후보, 검수 상태를 구조화하는 작업 절차를 정의한다.

## 1. 기본 원칙

1. 원문 EPUB/PDF는 공개 저장소에 커밋하지 않는다.
2. 저장소에는 직접 작성한 설명, 요약, 짧은 인용, 출처 위치, 태그, 검수 상태만 저장한다.
3. 인용문은 반드시 원문 대조 과정을 거쳐 `verified` 상태로 전환한다.
4. AI가 생성한 설명과 인용 후보는 초안으로 간주한다.
5. 책 설명과 인용 데이터는 분리한다.

## 2. 처리 단위

책 한 권은 다음 단위로 처리한다.

1. 원문 파일 확보
2. 메타데이터 입력
3. 본문 텍스트 추출
4. 장/절/페이지 구조 정리
5. 장별 요약 작성
6. 전체 상세 설명 작성
7. 인용 후보 추출
8. 원문·페이지·문맥 검수
9. JSON/JSONL 데이터 저장
10. 저장소 반영

## 3. 권장 파일 배치

```txt
private_sources/
  book_title.epub
  book_title.pdf

data/books/
  book_id.json

data/quotes/
  book_id.quotes.jsonl

data/topics/
  topic_id.json
```

## 4. 상태값

### book status

- `not_started`: 아직 처리하지 않음
- `source_ready`: 원문 파일은 준비됨
- `extracted`: 텍스트 추출 완료
- `summarized`: 요약 완료
- `quote_candidates_ready`: 인용 후보 생성 완료
- `reviewing`: 사람이 검수 중
- `verified`: 검수 완료
- `needs_revision`: 수정 필요

### quote confidence

- `candidate`: 자동 추출된 후보
- `needs_check`: 원문 대조 필요
- `verified`: 원문·페이지·문맥 확인 완료
- `rejected`: 사용하지 않기로 결정

## 5. 권장 처리 흐름

처음부터 전체 도서를 한 번에 처리하지 않는다.

1. EPUB 1권
2. 텍스트 기반 PDF 1권
3. OCR이 필요한 스캔 PDF 1권

위 세 유형을 샘플로 처리해 추출·요약·인용 품질을 검증한다. 이후 10권 단위로 배치 처리한다.

## 6. 검수 체크리스트

- 인용문이 원문과 정확히 일치하는가?
- 페이지 또는 EPUB location이 맞는가?
- 문맥이 왜곡되지 않았는가?
- 인용 길이가 과도하지 않은가?
- 번역본 인용인지 원서 인용인지 구분되어 있는가?
- 동일 인용이 중복 저장되지 않았는가?
- 주제 태그가 검색 목적에 맞게 붙었는가?
