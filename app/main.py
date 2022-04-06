import uvicorn

from fastapi import FastAPI
from app.api import api_router
from app.api.airlines import unprocessable_entity_exception_handler, UnprocessableEntityException, NotFoundException, not_found_exception_handler

app = FastAPI(title="AirlineAPI")
app.include_router(api_router, prefix= "/api")
app.add_exception_handler(UnprocessableEntityException, unprocessable_entity_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)