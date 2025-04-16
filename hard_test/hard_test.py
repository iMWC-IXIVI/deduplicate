from locust import HttpUser, constant, task, between


data = {
    'user': 'some_data',
    'user2': 'some_data',
    'user3': 'some_data',
    'user4': 'some_data',
    'user5': 'some_data',
    'user6': 'some_data',
    'user7': 'some_data',
    'user8': 'some_data',
    'user9': 'some_data',
    'user10': 'some_data',
    'user11': 'some_data',
    'user12': 'some_data',
    'user13': 'some_data',
}


class HardTest(HttpUser):
    wait_time = between(0.2, 0.3)

    @task
    def send_event(self):
        self.client.post('/service-event/', json=data)
