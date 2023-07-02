from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.auth.routes
import src.posts.routes
from src.auth.models import User
from src.posts.models import Post, LikeOrDislikePost

fastapi = FastAPI()

fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi.include_router(src.auth.routes.router)
fastapi.include_router(src.posts.routes.router)


@fastapi.on_event("startup")
def startup():
    User.create_table()
    Post.create_table()
    LikeOrDislikePost.create_table()
