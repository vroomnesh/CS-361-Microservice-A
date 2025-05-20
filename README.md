# CS-361-Microservice-A

This microservice is a recent activity tracker, that provides weekly listening activity summaries to a user.

## Communication Contract

### 1. How to PROGRAMMATICALLY REQUEST Data

- **HTTP Method**: `GET`
- **URL**: `/activity`
- **Query Parameters**:
  - `user_id` (string, **required**) — user's unique ID
  - `week_start` (string, **required**) — ISO date `YYYY-MM-DD` marking the start of the 7‑day window 
  - `media_type` (string, *optional*, `"song"` or `"podcast"`)

### Example REQUEST (Python)

import http.client  
import json

### 1) Open connection
conn = http.client.HTTPConnection("localhost", 8080)

### 2) Build path with query parameters
params = "user_id=1234&week_start=2025-05-01&media_type=song"  
path = f"/activity?{params}"

### 3) Send GET request
conn.request("GET", path)

### 4) Get the response
response = conn.getresponse()
print(response.status, response.reason)  # e.g. "200 OK"

### 5) Read raw body
raw_body = response.read().decode("utf-8")  
conn.close()


### 1. How to PROGRAMMATICALLY REQUEST Data

The service returns JSON with exactly two top‑level fields:

| Field             | Type    | Description                                     |
|-------------------|---------|-------------------------------------------------|
| `total_hours`     | number  | Sum of all durations in the 7‑day window        |
| `recent_activity` | array   | Up to 5 of the most recent events, newest first |

Each element of `recent_activity` has:

| Field       | Type    | Description                             |
|-------------|---------|-----------------------------------------|
| `title`     | string  | Song or podcast title                   |
| `artist`    | string  | Artist name or podcast hosts            |
| `type`      | string  | `"song"` or `"podcast"`                 |
| `timestamp` | string  | ISO 8601 datetime with `Z` timezone     |

### Example RECEIVE (Python)

import json

### Suppose `raw_body` is the response body from your GET /activity call
data = json.loads(raw_body)

print("Total hours:", data["total_hours"])  
for ev in data["recent_activity"]:
    print(f"{ev['timestamp']}: {ev['title']} ({ev['type']}) by {ev['artist']}")

