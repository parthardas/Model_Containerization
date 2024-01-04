import os
import sys
import time
import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from routes.routes import router 

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.getLogger().setLevel(logging.INFO)

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    logging.info("Running the app in debug mode.")
    uvicorn.run(app, host='0.0.0.0', port=8000)
