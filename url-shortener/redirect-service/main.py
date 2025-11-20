from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import redis, os, requests

app = FastAPI()
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
ANALYTICS_HOST = os.getenv("ANALYTICS_HOST", "analytics")
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

@app.get("/{code}")
def redirect(code: str):
    url = r.get(f"url:{code}")
    if not url:
        raise HTTPException(status_code=404, detail="Not found")
    # fire-and-forget analytics (best-effort)
    try:
        requests.post(f"http://{ANALYTICS_HOST}:8000/log/{code}", timeout=0.5)
    except Exception:
        pass
    return RedirectResponse(url)
