from fastapi import FastAPI, Query
from threading import Thread, Event
from ultralytics import YOLO

app = FastAPI()

# Dictionary to keep track of threads and their stop events
detection_threads = {}

def run_yolo_detection(stream_url: str, stop_event: Event):
    print(f"[INFO] Starting detection for: {stream_url}")
    model = YOLO("yolo11n.pt")
    results = model(stream_url, show=True, stream=True)
    for result in results:
        if stop_event.is_set():
            print(f"[INFO] Stopping detection for: {stream_url}")
            break
        # Process the result as needed

@app.get("/start-detection")
def start_detection(url: str = Query(..., description="Stream URL for YOLO detection")):
    if url in detection_threads:
        return {"status": "already_running", "message": f"Detection already running for {url}"}
    stop_event = Event()
    thread = Thread(target=run_yolo_detection, args=(url, stop_event))
    thread.start()
    detection_threads[url] = (thread, stop_event)
    return {"status": "started", "message": f"Started YOLO detection for {url}"}

@app.get("/stop-detection")
def stop_detection(url: str = Query(..., description="Stream URL to stop YOLO detection")):
    if url not in detection_threads:
        return {"status": "not_running", "message": f"No detection running for {url}"}
    thread, stop_event = detection_threads[url]
    stop_event.set()
    thread.join()
    del detection_threads[url]
    return {"status": "stopped", "message": f"Stopped YOLO detection for {url}"}
