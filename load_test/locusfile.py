from locust import HttpUser, task, between
from random import randint


class WebSiteTestUser(HttpUser):
    wait_time = between(0.5, 3.0)
    users = []

    def on_start(self):
        pass

    def on_stop(self):
        pass

    @task(5)
    def login(self):
        rand_idx = randint(0, len(self.users) - 1)
        email = self.users[rand_idx]
        body = {
            "email": email
        }
        self.client.post("http://0.0.0.0:3000/login", json=body)

    @task(1)
    def register(self):
        random_int = randint(0, 100000)
        email = f"user_test_{random_int}"
        body = {
            "email": email,
            "name": f"user {random_int}",
            "lastname": "test"
        }
        result = self.client.post("http://0.0.0.0:3000/register", json=body)
        if result.status_code == 200:
            self.users.append(email)

    # @task(15)
    # def get_item(self):
    #     self.client.get(f"http://0.0.0.0:3000/items/{randint(100, 10000)}")

    @task(10)
    def search(self):
        self.client.get(f"http://0.0.0.0:3000/items")

    @task(3)
    def create_order(self):
        body = {"item_id": str(randint(100, 10000))}
        self.client.post(f"http://0.0.0.0:3000/orders", json=body)

    @task(5)
    def create_payment(self):
        body = {"item_id": str(randint(100, 10000))}
        self.client.post(f"http://0.0.0.0:3000/payments", json=body)

