# Results

## Live Deployment

Render URL:

https://youtube-crawler-task.onrender.com

## GitHub Repository

https://github.com/SurajVRaikar/youtube-crawler-task

## Health Check

Endpoint:

https://youtube-crawler-task.onrender.com/health

Response:

```json
{
  "ok": true
}
```

This confirms the FastAPI application is running successfully.

## Queue Growth

Initial queue size:

* Count = 0

After the crawler executed:

* Count = 26

After additional scheduled runs:

* Count = 65

This demonstrates that the scheduler continuously discovers and stores new YouTube videos matching the configured keyword.

## Pagination

The crawler uses YouTube API pagination through the `nextPageToken` field.

Multiple pages of results are processed during each crawl cycle, ensuring the crawler does not stop at the first page of search results.

## Perceptual Deduplication (pHash)

For each video:

1. Thumbnail is downloaded.
2. Perceptual hash (pHash) is generated.
3. The generated hash is compared against previously stored hashes.
4. Duplicate items are skipped.

Example stored record:

```json
{
  "video_id": "mh7X6tQ4jJs",
  "title": "...",
  "thumbnail_url": "...",
  "phash": "8fe35035341e7ad8"
}
```

If another video produces the same perceptual hash, it is treated as a duplicate and is not added to the queue.

## Scheduler Verification

Scheduler interval:

* Every 1 minute

Deployment logs confirm:

```
Scheduler started every 1 minutes
```

This verifies that scheduled crawling is running automatically on the deployed Render service.

## Conclusion

The application successfully:

* Queries the YouTube Data API v3
* Handles pagination
* Downloads thumbnails
* Generates perceptual hashes (pHash)
* Deduplicates previously seen content
* Persists results in the queue
* Runs continuously on a deployed Render service


















