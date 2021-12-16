import os
from typing import Optional

import router.student_router as student_router
import uvicorn
from bson.objectid import ObjectId
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field

DB_URL = os.getenv("DB_URL")
DB_NAME = os.getenv("DB_NAME")

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    print(app.mongodb_client)
    app.db = app.mongodb_client[DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(student_router.router, prefix="/student")


def main():
    print("DB_URL: ", DB_URL)
    print("DB_NAME: ", DB_NAME)
    uvicorn.run(app, port=8080, host="0.0.0.0")


if __name__ == "__main__":
    main()
