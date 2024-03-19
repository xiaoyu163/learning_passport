from locustfile import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def login(self):
        self.client.get("https://learning-passport-633550e98be1.herokuapp.com/login")
        