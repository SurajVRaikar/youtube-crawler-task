# Results

Keyword: movie clips

Implemented Features

- FastAPI application
- Health endpoint (/health)
- Queue endpoint (/queue)
- APScheduler background crawler
- YouTube Data API v3 integration
- Pagination using nextPageToken
- Queue persistence using scan_queue.json
- Video ID deduplication
- Perceptual deduplication using pHash

Testing

- Successfully fetched videos from YouTube.
- Successfully stored queue data.
- Successfully generated pHash values for thumbnails.
- Successfully prevented duplicate entries.

Current Status

Application is running successfully and crawling videos automatically every minute.







