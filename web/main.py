import os
import time
from random import randint, sample

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, HTTPException, Request
from datadog import initialize, statsd

initialize(statsd_host=os.environ.get('DATADOG_HOST'))


# Mock data
def get_mock_items(size=1000000):
    items_ids = {str(i): i for i in range(size)}
    return items_ids, get_mock_items_price(items_ids)


def get_mock_items_price(items_ids):
    return {key: randint(100, 10000) for key in items_ids}

users = {}
items, items_prices = get_mock_items()
orders = {}
payments = []
MAX_ITEMS_TO_RETURN = 20


# Heartbeat
def job():
    statsd.increment("web.ping")


scheduler = BackgroundScheduler()
scheduler.add_job(func=job, trigger="cron", minute="*", hour="*")
scheduler.start()


# API
app = FastAPI()


@app.middleware("http")
async def before_request(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        statsd.increment(f"web.response_status_code",
                         tags=[f"status_code:500", f"endpoint:{request.url.path}"])
        return e
    process_time = time.time() - start_time
    statsd.increment("web.response_time",
                     tags=[f"endpoint:{request.url.path}"],
                     value=process_time * 1000.0)
    if response.status_code >= 300:
        statsd.increment(f"web.response_status_code",
                         tags=[f"status_code:{response.status_code}", f"endpoint:{request.url.path}"])
    statsd.increment("web.response_amount")
    return response


@app.get("/")
def read_root():
    statsd.increment("web.ping")
    return "ping"


@app.post("/login")
def login(user: dict):
    if user["email"] in users:
        statsd.increment("web.active_user")
    else:
        statsd.increment("web.error_login")
        raise HTTPException(status_code=404, detail="user not found")
    return user


@app.post("/register")
def register(user: dict):
    if user["email"] in users:
        statsd.increment("web.error_register")
        raise HTTPException(status_code=400, detail="user is already registered")
    else:
        users[user["email"]] = user
        statsd.increment("web.new_user")
        return user


@app.post("/orders")
def send_orders(order: dict):
    statsd.increment("web.new_order")
    order_id = order["item_id"] + str(randint(100, 10000))
    orders[order_id] = items_prices[order["item_id"]]
    return {"order_id": order_id}


@app.post("/payments")
def pay(order: dict):
    statsd.increment("web.new_payment")
    statsd.increment("web.billing", value=items_prices[order["item_id"]])
    payments.append(order["item_id"])
    return {"payment_id": order["item_id"]}


@app.get("/items")
def read_items():
    return sample(list(items.keys()), MAX_ITEMS_TO_RETURN)


@app.get("/items/{item_id}")
def read_item(item_id: str = None):
    if item_id == None:
        return list(items)
    return {"item_id": items[item_id]}


if __name__ == "__main__" and os.getenv("SCOPE") == "DEV":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
