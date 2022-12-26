class event:
    def __init__(self, year, month, day, hour, minute, eventname):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.event_name = eventname

    def printevent(self):
        print(f"Event printing...\n"
            f"Date: {self.year}.{self.month}.{self.day}\n"
              f"Time: {self.hour}:{self.minute}\n"
              f"Event: {self.event_name}\n"
        )