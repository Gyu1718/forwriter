# Data Schema

ForWriter Citation Library는 책 정보와 인용 정보를 분리해서 관리한다.

## 1. Book record

위치:

```txt
data/books/{book_id}.json
```

예시:

```json
{
  "book_id": "sample_book",
  "title_ko": "샘플 도서",
  "title_original": "Sample Book",
  "author": "Author Name",
  "translator": "",
  "publisher": "",
  "published_year": "",
  "edition": "",
  "language": "ko",
  "source_type": "epub",
  "source_file": "private_sources/sample_book.epub",
  "isbn": "",
  "status": "not_started",
  "short_description": "",
  "detailed_description": "",
  "main_argument": "",
  "chapter_summary": [],
  "keywords": [],
  "themes": [],
  "recommended_use": [],
  "review_status": "needs_human_review",
  "created_at": "",
  "updated_at": ""
}
```

### Field notes

| field | meaning |
| --- | --- |
| `book_id` | 파일명과 연결되는 고유 식별자. 영문 소문자, 숫자, 언더스코어 권장 |
| `title_ko` | 한국어 제목 |
| `title_original` | 원제 |
| `source_type` | `epub`, `pdf_text`, `pdf_scan`, `manual` 중 하나 |
| `source_file` | 로컬 원문 파일 경로. 공개 저장소에는 파일 자체를 올리지 않음 |
| `short_description` | 목록용 2~3문장 소개 |
| `detailed_description` | 책의 핵심 논지와 구조를 설명하는 상세 소개 |
| `main_argument` | 책 전체의 중심 논지 |
| `chapter_summary` | 장별 요약 배열 |
| `recommended_use` | 설교, 칼럼, 연구, 에세이 등 활용 포인트 |

## 2. Chapter summary object

```json
{
  "chapter_id": "ch01",
  "title": "1장 제목",
  "location": "pp. 1-24",
  "summary": "",
  "main_points": [],
  "keywords": []
}
```

## 3. Quote record

위치:

```txt
data/quotes/{book_id}.quotes.jsonl
```

JSONL은 한 줄에 하나의 JSON 객체를 둔다.

```json
{"quote_id":"sample_book_q001","book_id":"sample_book","quote":"짧은 인용문을 여기에 둔다.","page":"12","location":"ch01","chapter":"1장","theme":["grace","church"],"note":"글쓰기 활용 메모","confidence":"needs_check","verified_by":"","created_at":"","updated_at":""}
```

### Quote field notes

| field | meaning |
| --- | --- |
| `quote_id` | `{book_id}_q001` 형식 권장 |
| `quote` | 짧은 인용문 |
| `page` | PDF 또는 인쇄본 페이지 |
| `location` | EPUB CFI, 장/절 위치, 또는 내부 위치 정보 |
| `theme` | 검색용 주제 태그 |
| `note` | 왜 이 인용이 중요한지에 대한 메모 |
| `confidence` | `candidate`, `needs_check`, `verified`, `rejected` |

## 4. Topic record

위치:

```txt
data/topics/{topic_id}.json
```

```json
{
  "topic_id": "grace",
  "name_ko": "은혜",
  "name_en": "grace",
  "description": "",
  "related_topics": [],
  "representative_books": [],
  "representative_quotes": []
}
```

## 5. Naming conventions

- 파일명은 가능하면 영문 소문자와 언더스코어만 사용한다.
- 한 책의 `book_id`, 책 JSON 파일명, 인용 JSONL 파일명은 서로 일치시킨다.
- 예: `bonhoeffer_discipleship.json`, `bonhoeffer_discipleship.quotes.jsonl`
