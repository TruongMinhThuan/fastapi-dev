from typing import Union

from fastapi import FastAPI
import uvicorn
from celery import Celery
import time


app = FastAPI()


celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

@app.get("/")
def read_root():
    return {"Hello": "World Trigger"}


@app.get("/thread1")
def read_item():
    print("T1 start")
    time.sleep(15)
    print("T1 end")
    return {"data": "T1"}


@app.get("/thread2")
def read_item():
    print("T2 start")
    time.sleep(5)
    print("T2 end")
    return {"data": "T2"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@celery.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y


if __name__ == '__main__':
    print("Hello World")
    uvicorn.run(app, port=8000, host='0.0.0.0')
