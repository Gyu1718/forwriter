# Book Intake Guide

이 문서는 여러 권의 EPUB/PDF를 ForWriter Citation Library에 등록하기 위한 도서 목록 입력 절차를 정리한다.

## 1. 목적

책 원문을 곧바로 처리하기 전에 먼저 `data/intake/books_to_process.csv`에 도서 목록을 정리한다. 이 CSV를 기준으로 책별 JSON 골격과 전체 인덱스를 자동 생성한다.

## 2. 입력 파일

```txt
data/intake/books_to_process.csv
```

## 3. CSV 필드

| field | required | description |
| --- | --- | --- |
| `book_id` | yes | 책 고유 ID. 영문 소문자, 숫자, 언더스코어 사용 권장 |
| `title_ko` | yes | 한국어 제목 |
| `title_original` | no | 원제 |
| `author` | yes | 저자 |
| `translator` | no | 역자 |
| `publisher` | no | 출판사 |
| `published_year` | no | 출판 연도 |
| `edition` | no | 판본 정보 |
| `language` | yes | `ko`, `en`, `de`, `el`, `he` 등 |
| `source_type` | yes | `epub`, `pdf_text`, `pdf_scan`, `manual` |
| `source_file` | yes | 로컬 원문 파일 경로. 예: `private_sources/book.epub` |
| `isbn` | no | ISBN |
| `priority` | no | `high`, `normal`, `low` |
| `notes` | no | 작업 메모 |

## 4. book_id 규칙

권장 형식:

```txt
author_short_title
```

예시:

```txt
bonhoeffer_discipleship
augustine_confessions
lewis_mere_christianity
barth_church_dogmatics_1_1
```

한글, 공백, 특수기호는 피한다. 나중에 파일명, 인용 ID, 주제 연결에 사용되기 때문이다.

## 5. source_type 선택 기준

| source_type | meaning |
| --- | --- |
| `epub` | EPUB 파일. 장 구조 추출이 비교적 쉬움 |
| `pdf_text` | 텍스트 선택이 가능한 PDF |
| `pdf_scan` | 이미지 기반 스캔 PDF. OCR 필요 |
| `manual` | 원문 자동 추출 없이 사람이 직접 입력 |

## 6. 처리 순서

1. `books_to_process.csv`에 책 목록을 입력한다.
2. `scripts/generate_book_records.py`를 실행한다.
3. `data/books_index.json`과 `data/books/{book_id}.json`이 생성된다.
4. `scripts/validate_library.py`로 기본 구조를 검사한다.
5. 이후 원문 추출, 요약, 인용 후보 생성 작업으로 넘어간다.

## 7. 권장 시작 방식

처음에는 전체 목록을 한 번에 넣기보다 다음 세 유형을 먼저 넣는다.

1. EPUB 1권
2. 텍스트 기반 PDF 1권
3. OCR이 필요한 스캔 PDF 1권

이 세 권을 기준으로 추출 품질과 검수 흐름을 확인한 뒤, 10권 단위로 확장한다.
