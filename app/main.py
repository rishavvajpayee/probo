"""
Entrypoint for App
"""
import uvicorn

from fastapi import FastAPI
from api.endpoints.users import USER_ROUTES
from api.endpoints.markets import MARKETS_ROUTES
from api.endpoints.trades import TRADE_ROUTES

app = FastAPI()


@app.get("/")
def health():
    return {"msg": "Server looks good"}


app.include_router(USER_ROUTES, tags=["users"])
app.include_router(MARKETS_ROUTES, tags=["markets"])
app.include_router(TRADE_ROUTES, tags=["trades"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)