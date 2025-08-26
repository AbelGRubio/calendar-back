"""
Defines and initializes the FastAPI application, including route registration
and middleware setup.

This module serves as the main entry point for assembling the API structure
and exposing the application instance for use with ASGI servers.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from .configuration import __version__, CORS_ORIGINS
                            
from .routes import api_router, v1_router


APP = FastAPI(
    title="Calendar Backend",
    summary="Calendar Backend",
    version=__version__
)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["20/5seconds"]  
    )
APP.state.limiter = limiter

APP.add_middleware(SlowAPIMiddleware)

async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Too Many Requests"}
    )

APP.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)


APP.include_router(
    router=api_router,
    prefix='/api',
    tags=["Router 1: API endpoints"]
)


APP.include_router(
    router=v1_router,
    prefix='/v1',
    tags=["Router 2: V1 endpoints"]
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

