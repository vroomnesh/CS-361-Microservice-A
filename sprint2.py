from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
import os

app = Flask(__name__)

# --- Root & Health Endpoints ---
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Activity service is running"}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

# --- Local Dataset Loader ---
def load_local_dataset():
    return [
        {
            "user_id": "1234",
            "title": "The Spins",
            "artist": "Mac Miller",
            "type": "song",
            "timestamp": "2025-05-02T10:11:22Z",
            "duration_hours": 0.05
        },
        {
            "user_id": "1234",
            "title": "Whats Good with Miniminter and Randolph",
            "artist": "Miniminter & Randolph",
            "type": "podcast",
            "timestamp": "2025-05-07T12:00:00Z",
            "duration_hours": 1.0
        },
        {
            "user_id": "1234",
            "title": "Payphone",
            "artist": "Maroon 5",
            "type": "song",
            "timestamp": "2025-05-03T08:00:00Z",
            "duration_hours": 0.03
        },
        {
            "user_id": "1234",
            "title": "Feel It",
            "artist": "d4vd",
            "type": "song",
            "timestamp": "2025-05-04T09:00:00Z",
            "duration_hours": 0.02
        },
        {
            "user_id": "1234",
            "title": "Chemical",
            "artist": "Post Malone",
            "type": "song",
            "timestamp": "2025-05-05T12:00:00Z",
            "duration_hours": 0.02
        },
        {
            "user_id": "1234",
            "title": "3 Nights",
            "artist": "Dominic Fike",
            "type": "song",
            "timestamp": "2025-05-06T14:00:00Z",
            "duration_hours": 0.02
        }
    ]

# Initialize dataset
dataset = load_local_dataset()

# --- Activity Endpoint ---
@app.route('/activity', methods=['GET'])
def activity():
    user_id        = request.args.get('user_id')
    week_start_str = request.args.get('week_start')
    media_type     = request.args.get('media_type')  # optional

    # Validate required params
    if not user_id or not week_start_str:
        return jsonify({
            "error": "Missing required parameters 'user_id' and 'week_start'"
        }), 400

    try:
        week_start = datetime.fromisoformat(week_start_str)
        week_start = week_start.replace(tzinfo=timezone.utc)
    except ValueError:
        return jsonify({
            "error": "Invalid week_start format. Use ISO format YYYY-MM-DD"
        }), 400

    week_end = week_start + timedelta(days=7)

    # Filter by user_id (and optionally by media_type)
    user_events = [e for e in dataset if e['user_id'] == user_id]
    if media_type:
        user_events = [e for e in user_events if e['type'] == media_type]

    # Sum durations and collect events in window
    total_hours = 0.0
    parsed_events = []
    for e in user_events:
        try:
            ts = datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00'))
        except ValueError:
            continue
        if week_start <= ts < week_end:
            total_hours += e.get('duration_hours', 0)
            parsed_events.append((ts, e))

    # Sort descending by timestamp and limit to 5
    parsed_events.sort(key=lambda x: x[0], reverse=True)
    recent = [
        {
            "title": ev['title'],
            "artist": ev.get('artist'),
            "type": ev['type'],
            "timestamp": ev['timestamp']
        }
        for _, ev in parsed_events[:5]
    ]

    # Build response
    response = {
        "total_hours": round(total_hours, 2),
        "recent_activity": recent
    }
    if media_type:
        response['media_type'] = media_type

    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)