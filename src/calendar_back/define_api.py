"""
Defines and initializes the FastAPI application, including route registration
and middleware setup.

This module serves as the main entry point for assembling the API structure
and exposing the application instance for use with ASGI servers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .configuration import __version__, CORS_ORIGINS
                            
from .routes import api_router, v1_router

APP = FastAPI(
    title="REST API WITH EXAMPLES",
    summary="REST API WITH EXAMPLES",
    version=__version__
)


APP.include_router(
    router=api_router,
    prefix='/api',
    tags=["Service 1: API endpoints"]
)


APP.include_router(
    router=v1_router,
    prefix='/v1',
    tags=["Service 2: v1 endpoints"]
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
