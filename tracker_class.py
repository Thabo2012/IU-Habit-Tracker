class Habit:
    def __init__(self, habit_name: str, periodicity, date_created=None, logs=None, current_streak = None, target_streak= None):
        """
        :param habit_name: name of the habit
        :param periodicity: when was the habit performed eg weekly or daily
        :param date_created: The date the Habit was created
        :param logs: the date of Habit completion
        :param current_streak: current successfully completion progress of the habit
        :param target_streak: The intended consecutive streak by user
        """
        self.habit_name = habit_name
        self.periodicity = periodicity
        self.date_created = date_created
        self.logs = logs or []
        self.current_streak = current_streak
        self.target_streak = target_streak



    def __str__(self):
        return f" {self.habit_name}: {self.periodicity}: {self.date_created}: {self.logs}: {self.current_streak}: {self.target_streak}"
