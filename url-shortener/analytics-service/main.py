from fastapi import FastAPI
import redis, os

app = FastAPI()
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

@app.post("/log/{code}")
def log_click(code: str):
    r.incr(f"clicks:{code}")
    return {"status": "ok"}

@app.get("/stats/{code}")
def stats(code: str):
    clicks = r.get(f"clicks:{code}") or "0"
    url = r.get(f"url:{code}") or ""
    return {"code": code, "url": url, "clicks": int(clicks)}
