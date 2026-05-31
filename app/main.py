import os
import json
import requests

from PIL import Image
from io import BytesIO
import imagehash

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Keyword Crawler + Dedup")

KEYWORD = os.getenv("KEYWORD", "movie clips")
INTERVAL_MIN = int(os.getenv("INTERVAL_MIN", "1"))
YT_API_KEY = os.getenv("YT_API_KEY")

QUEUE_FILE = "scan_queue.json"


def load_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_queue(data):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/queue")
def get_queue():
    queue = load_queue()
    return {
        "count": len(queue),
        "items": queue
    }


def crawl_once():
    try:
        if not YT_API_KEY:
            print("YT_API_KEY missing")
            return

        url = "https://www.googleapis.com/youtube/v3/search"

        queue = load_queue()

        existing_ids = {
            item["video_id"]
            for item in queue
        }

        existing_hashes = {
            item.get("phash")
            for item in queue
            if item.get("phash")
        }

        next_page_token = None

        for _ in range(3):  # Pagination

            params = {
                "part": "snippet",
                "q": KEYWORD,
                "type": "video",
                "maxResults": 10,
                "key": YT_API_KEY
            }

            if next_page_token:
                params["pageToken"] = next_page_token

            response = requests.get(url, params=params)
            data = response.json()

            for item in data.get("items", []):

                video_id = item["id"]["videoId"]

                if video_id in existing_ids:
                    continue

                thumbnail_url = item["snippet"]["thumbnails"]["high"]["url"]

                img_data = requests.get(thumbnail_url).content
                img = Image.open(BytesIO(img_data))

                phash = str(imagehash.phash(img))

                if phash in existing_hashes:
                    continue

                video = {
                    "video_id": video_id,
                    "title": item["snippet"]["title"],
                    "thumbnail_url": thumbnail_url,
                    "phash": phash
                }

                queue.append(video)
                existing_ids.add(video_id)
                existing_hashes.add(phash)

            next_page_token = data.get("nextPageToken")

            if not next_page_token:
                break

        save_queue(queue)

        print(f"Queue size: {len(queue)}")

    except Exception as e:
        print("Crawler Error:", e)


@app.on_event("startup")
def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        crawl_once,
        "interval",
        minutes=INTERVAL_MIN
    )

    scheduler.start()

    print(
        f"Scheduler started every {INTERVAL_MIN} minutes"
    )