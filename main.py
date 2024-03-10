import os

import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from schemas import userPayload
from routers import get_user_info

load_dotenv()

app = FastAPI()


origins = ["*"]  # Allow requests from any origin

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


@app.get("/secure")
async def root(user: userPayload = Depends(get_user_info)):
    return {"message": f"Hello {user.username} you have the access to the following service: {user.realm_roles}"}


if __name__ == '__main__':
    uvicorn.run("main:app", host=os.getenv("APP_HOST", "localhost"), port=int(os.getenv("APP_PORT", 5000)), reload=True)
