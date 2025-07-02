import os
import requests
from ics import Calendar
from flask import Flask, jsonify, send_from_directory
from datetime import datetime
import pytz

app = Flask(__name__)

calendars = {
    "santiysergiocraftyo": "https://calendar.google.com/calendar/ical/santiysergiocraftyo%40gmail.com/private-c6119193fa54b29d00834ddaed15773d/basic.ics",
    "Familia": "https://calendar.google.com/calendar/ical/family09544694029503912378%40group.calendar.google.com/private-e6ec0b523158d50e5f66fe429403578b/basic.ics",
    "FC Barcelona": "https://calendar.google.com/calendar/ical/b31f219135d81681a6e0c5ab745ce1b72c527e5ec99f153828310f517990bade%40group.calendar.google.com/private-035eb24a9595443cde35462c9e5177ce/basic.ics",
    "España": "https://calendar.google.com/calendar/ical/8n8ctvj3uu2ltaq1objjdtn41g%40group.calendar.google.com/public/basic.ics",
    "Real Madrid": "https://calendar.google.com/calendar/ical/dptm8psv9fk6khmphttvmrapp4%40group.calendar.google.com/public/basic.ics",
    "Sevilla": "https://calendar.google.com/calendar/ical/4g31en3kv4eqeuvbl8hrtd87v0%40group.calendar.google.com/public/basic.ics",
}

madrid_tz = pytz.timezone("Europe/Madrid")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/events')
def get_events():
    now = datetime.now(madrid_tz)
    all_events = []
    for name, url in calendars.items():
        try:
            r = requests.get(url)
            r.raise_for_status()
            c = Calendar(r.text)
            future_events = [e for e in c.events if e.begin.astimezone(madrid_tz) >= now]
            events_sorted = sorted(future_events, key=lambda e: e.begin)[:5]
            for e in events_sorted:
                all_events.append({
                    "calendar": name,
                    "summary": e.name,
                    "start": e.begin.astimezone(madrid_tz).isoformat(),
                    "end": e.end.astimezone(madrid_tz).isoformat(),
                })
        except Exception as ex:
            all_events.append({
                "calendar": name,
                "error": f"No se pudo cargar el calendario: {ex}"
            })
    all_events = sorted(all_events, key=lambda x: x.get("start", ""))
    return jsonify(all_events)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
