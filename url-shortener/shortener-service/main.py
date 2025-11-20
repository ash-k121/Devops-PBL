from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import redis, uuid, os

app = FastAPI()
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

class Req(BaseModel):
    url: HttpUrl

@app.post("/shorten")
def shorten(req: Req):
    code = str(uuid.uuid4())[:6]
    r.set(f"url:{code}", str(req.url))   # ✅ convert HttpUrl → string
    return {"code": code, "short_url": f"http://{os.getenv('DOMAIN','localhost')}/{code}"}
