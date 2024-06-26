from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

import sentencepiece as _sentencepiece
import torch as _torch
import tensorflow as _tensorflow

# imports that have to be loaded before lightning to avoid segfaults
_sentencepiece
_tensorflow
_torch


from openad_model_generation_service.call_generation_services import service_requester, get_services  # noqa: E402
from pydantic import BaseModel  # noqa: E402


app = FastAPI()

requester = service_requester()


@app.get("/health", response_class=HTMLResponse)
async def health():
    return "UP"


@app.post("/service")
def service(property_request: dict):
    print("\n-------------STARING NEW REQUEST-------------\n")
    result = requester.route_service(property_request)

    return result


def main():
    import uvicorn
    import torch

    if torch.cuda.is_available():
        print(f"\n[i] cuda is available: {torch.cuda.is_available()}")
        print(f"[i] cuda version: {torch.version.cuda}\n")
        print(f"[i] device name: {torch.cuda.get_device_name(0)}")
        print(f"[i] torch version: {torch.__version__}\n")
    uvicorn.run(app, host="0.0.0.0", port=8080)

@app.get("/service")
async def get_service_defs():
    """return list of services definitions"""
    # get service list
    service_list: list = get_services()
    return JSONResponse(service_list)


if __name__ == "__main__":
    main()
