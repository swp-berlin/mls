# API Documentation

The API is available under `/api/v1/`.

## Endpoints

### Extract

**URL:** `/extract/`

**Methods:**
- `POST`
- `PUT`

**Description:**
Extracts text from an uploaded file.

**Request:**
- `Content-Type`: The content type of the file being uploaded.
- `file`: The file to be processed.

**Responses:**
- `200 OK`: Returns the extracted text in plain text format.
- `415 Unsupported Media Type`: If the media type is not supported.

**cURL Example:**

```sh
curl -X POST -H "Content-Type: application/pdf" -H "Content-Disposition: attachment;filename=test.pdf" -F "file=@test.pdf" http://localhost:8080/api/v1/extract/
```

Filename in URL:

```sh
curl -G --data-urlencode "query=your query string" http://localhost:8080/query-embed/
```

### Embedding

**URL:** `/embedding/`

**Methods:**
- `POST`
- `PUT`

**Description:**
Generates an embedding from the extracted text of an uploaded file.

**Request:**
- `Content-Type`: The content type of the file being uploaded.
- `file`: The file to be processed.

**Responses:**
- `200 OK`: Returns the generated embedding.
- `204 No Content`: If no embedding could be generated.
- `415 Unsupported Media Type`: If the media type is not supported.

** cURL Example:**

Filename as header:

```sh
 curl -X POST -H "Content-Type: application/pdf" -H "Content-Disposition: attachment;filename=test.pdf" -F "file=@test.pdf" http://localhost:8080/api/v1/embedding/
```

Filename in URL:

```sh
curl -X PUT -H "Content-Type: application/pdf"  -F "file=@test.pdf" http://localhost:8080/api/v1/embedding/test.pdf
```


### Query Embedding

**URL:** `/query-embed/`

**Methods:**
- `GET`

**Description:**
Generates an embedding for a given query.

**Request:**
- `query`: The query string to be embedded.

**Responses:**
- `200 OK`: Returns the generated embedding.
- `400 Bad Request`: If the query parameter is missing or invalid.

**cURL Example:**

```sh
curl -G --data-urlencode "query=your query string" http://localhost:8080/api/v1/query-embed/
```
