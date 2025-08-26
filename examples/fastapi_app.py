# This is an illustrative example for the Loom project.
# It defines an async FastAPI app but the loom runner expects async main() for demo.
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
async def hello():
    return {'hello':'world'}

async def main():
    # run uvicorn in the same process; use --reload disabled for demo
    config = uvicorn.Config(app, host='127.0.0.1', port=8000, log_level='info')
    server = uvicorn.Server(config)
    await server.serve()
