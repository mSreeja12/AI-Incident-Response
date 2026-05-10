from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import json
from datetime import datetime

from classifier import classify_log, severity_prediction
from rag_engine import generate_rca

LOG_FILE = "server.log"
INCIDENT_FILE = "incidents.json"

last_processed_log = ""


def save_incident(incident):
    try:
        with open(INCIDENT_FILE, "r") as file:
            incidents = json.load(file)
    except:
        incidents = []

    incidents.insert(0, incident)

    with open(INCIDENT_FILE, "w") as file:
        json.dump(incidents, file, indent=4)


class LogHandler(FileSystemEventHandler):

    def on_modified(self, event):
        global last_processed_log

        if not event.src_path.endswith(LOG_FILE):
            return

        try:
            with open(LOG_FILE, "r") as file:
                lines = file.readlines()
        except:
            return

        if not lines:
            return

        latest_log = lines[-1].strip()

        # Ignore empty logs
        if not latest_log or len(latest_log) < 5:
            return

        # Ignore duplicate triggers
        if latest_log == last_processed_log:
            return

        last_processed_log = latest_log

        category = classify_log(latest_log)
        severity = severity_prediction(latest_log)
        analysis = generate_rca(latest_log)

        incident = {
            "log": latest_log,
            "category": category,
            "severity": severity,
            "analysis": analysis,
            "time": datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")
        }

        save_incident(incident)

        print("New incident saved:", incident["category"])
        print("Log:", latest_log)


event_handler = LogHandler()
observer = Observer()
observer.schedule(event_handler, path=".", recursive=False)
observer.start()

print("Watching server.log for new incidents...")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    observer.stop()

observer.join()