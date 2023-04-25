import pendulum

class Broadcast:
    def __init__(self, title: str, day: int, hour: int, minute: int):
        self.title = title
        self.day = day
        self.hour = hour
        self.minute = minute

    def get_start_time(self):
        return pendulum.now().next(self.day).set(hour=self.hour, minute=self.minute).to_iso8601_string()