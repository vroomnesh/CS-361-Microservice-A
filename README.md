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

```python
import http.client  
import json

# 1) Open connection
conn = http.client.HTTPConnection("localhost", 8080)

# 2) Build path with query parameters
params = "user_id=1234&week_start=2025-05-01&media_type=song"  
path = f"/activity?{params}"

# 3) Send GET request
conn.request("GET", path)

# 4) Get the response
response = conn.getresponse()
print(response.status, response.reason)  # e.g. "200 OK"

# 5) Read raw body
raw_body = response.read().decode("utf-8")  
conn.close()
```

### 2. How to PROGRAMMATICALLY RECEIVE Data

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

```python
import json

# Suppose `raw_body` is the response body from your GET /activity call
data = json.loads(raw_body)

print("Total hours:", data["total_hours"])
for ev in data["recent_activity"]:
    print(f"{ev['timestamp']}: {ev['title']} ({ev['type']}) by {ev['artist']}")
```
### 3. UML Sequence Diagram

sequenceDiagram
    autonumber
    participant Client as Program making request
    participant Service as ActivityService
    participant DB as DataStore

    note left of Client
      • user_id (required)  
      • week_start (required)  
      • media_type (optional)
    end note

    Client->>Service: GET /activity?user_id=1234&week_start=2025-05-01&media_type=song
    Service->>DB: queryActivities(user_id, start, end, media_type)
    DB-->>Service: return activityRecords
    Service->>Service: calculate total_hours  
    Service->>Service: select up to 5 recent events
    Service-->>Client: 200 OK + JSON { total_hours, recent_activity }

    note right of Service
      • filters by media_type if provided  
      • orders recent_activity by timestamp desc  
    end note

