import json
import random
from locust import HttpUser, task, between


with open('hard_test/datas/datas.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)


def random_data():
    while True:
        yield random.choice(all_data)


data_gen = random_data()


class HardTest(HttpUser):
    wait_time = between(0.2, 0.3)

    @task
    def send_event(self):
        data = next(data_gen)
        self.client.post('/service-event/', json=data)
