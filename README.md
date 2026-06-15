# forwriter

글을 쓰는 사람들을 위한 자료 정리 저장소입니다.

## ForWriter Citation Library

이 저장소는 책 원문을 보관하는 공간이 아니라, 글쓰기와 연구에 활용할 수 있는 책 설명, 주제 태그, 짧은 인용, 출처 위치, 검수 상태를 구조화하는 공간입니다.

## 기본 원칙

- EPUB/PDF 원문 파일은 공개 저장소에 올리지 않습니다.
- OCR 결과 전체나 책 전체 텍스트 추출본도 커밋하지 않습니다.
- 공개 저장소에는 직접 작성한 설명, 요약, 짧은 인용, 페이지/위치 정보, 태그, 검수 상태만 둡니다.
- AI가 추출한 인용 후보는 원문 대조 전까지 `verified`로 표시하지 않습니다.

## 구조

```txt
docs/
  workflow.md
  schema.md
  citation_policy.md

data/
  books_index.json
  books/
    sample_book.json
  quotes/
    sample_book.quotes.jsonl
  topics/
    sample_topic.json

private_sources/
  .gitkeep
```

## 처리 흐름

1. `private_sources/`에 로컬 원문 파일을 둡니다.
2. `data/books_index.json`에 책 목록과 처리 상태를 기록합니다.
3. 책별 메타데이터와 설명은 `data/books/{book_id}.json`에 저장합니다.
4. 인용 후보는 `data/quotes/{book_id}.quotes.jsonl`에 저장합니다.
5. 사람이 원문·페이지·문맥을 검수한 뒤 인용 상태를 `verified`로 변경합니다.

## 문서

- [Workflow](docs/workflow.md)
- [Schema](docs/schema.md)
- [Citation Policy](docs/citation_policy.md)
