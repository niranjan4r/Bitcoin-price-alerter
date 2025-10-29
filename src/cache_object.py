import datetime as datetime
class AlertCache:
    def __init__(self):
        self.last_threshold=None
        self.last_week=None

    @staticmethod
    def current_week(): #returns the current year and week number as a tuple. For eg (2025,34)
        today = datetime.datetime.now(datetime.timezone.utc)
        return today.isocalendar()[:2]

    def reset_week(self): #resets the last threshold if a new week is detected
        if self.current_week()!=self.last_week:
            print('New week detected, resetting last threshold')
            self.last_week=self.current_week()
            self.last_threshold=None