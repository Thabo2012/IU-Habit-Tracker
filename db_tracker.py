import sqlite3
from datetime import datetime, timedelta
from tracker_class import Habit

class DBHandler():
    """Create connection on main db"""
    def __init__(self, db_name = "main.db"):
        self.db = sqlite3.connect(db_name)
        self.cur = self.db.cursor()

    def cursor(self):
        return self.db.cursor()

    def commit(self):
        return self.db.commit()

    def create_habits_tables(self):
        self.cur.execute(""" 
        CREATE TABLE IF NOT EXISTS habits_tables(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_name TEXT not null UNIQUE,
        periodicity TEXT not null,  
        date_created TEXT NOT NULL,
        current_streak INTEGER DEFAULT 0,
        target_streak INTEGER
        )    
        """)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS completion(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        date_completed TEXT NOT NULL,
        FOREIGN KEY(habit_id) REFERENCES habits_tables(id) 
        )
        """)
        self.db.commit()

    def add_habits_into_tables(self, habits):
        """INSERTING PREDEFINED HABITS LOGS INTO tables"""
        if isinstance(habits, Habit):
            habits = [habits]

        for habit in habits:
            self.cur.execute(
                """INSERT OR IGNORE INTO habits_tables 
                (habit_name, periodicity, date_created, current_streak, target_streak) 
                VALUES (?, ?, ?, ?, ?)""",
                (habit.habit_name, habit.periodicity, habit.date_created, habit.current_streak, habit.target_streak)
            )

        self.db.commit()

    def add_logs(self, habit, habit_id):
        """Insert completion logs for a habit into the completion table."""
        for log_date in habit.logs:
            self.cur.execute(
                "INSERT INTO completion (habit_id, date_completed) VALUES (?, ?)",
                (habit_id, log_date.isoformat())
            )
        self.db.commit()


    def habit_exists(self, habit_name):
        if not habit_name:
            return False

        self.cur.execute("SELECT 1 FROM habits_tables WHERE lower(habit_name) = lower(?)",
                         (habit_name.strip().lower(),)
                         )
        return self.cur.fetchone() is not None

    def create_new_habit(self):
        while True:
            habit_name = input("Enter habit name: ").strip().lower()
            if self.habit_exists(habit_name):
                print("Habit already exists, please enter a new one: ")
            else:
                break
        while True:
            periodicity = input("Enter periodicity (daily or weekly): ").strip().lower()
            if periodicity in ["daily", "weekly"]:
                break
            print("Please enter 'daily' or 'weekly'.")

        while True:
            try:
                target_streak = int(input("Enter the target streak, any number of choice: ").strip())
                break

            except ValueError:
                print("Please enter valid number: ")

        new_habit = Habit(
            habit_name=habit_name,
            periodicity=periodicity,
            date_created=datetime.now(),
            target_streak=target_streak,
            current_streak = 0

        )

        self.add_habits_into_tables([new_habit])
        print(f"Habit '{habit_name}' added successfully.")

    def get_all_habits(self):
        """List all the habits in the app"""
        self.cur.execute("SELECT habit_name, periodicity, date_created FROM habits_tables")
        habits = self.cur.fetchall()

        results = []
        for habit_id, habit_name, periodicity, date_created in habits:
            self.cur.execute("SELECT COUNT(*) FROM completion WHERE habit_id = ?", (habit_id,))
            log_count = self.cur.fetchone()
            results.append((habit_name, date_created, periodicity, log_count))
        return results

    """Add new Habit to the habits table"""

    def update_habit(self, habit_name, attribute, value):
        if attribute not in ("habit_name", "periodicity"):
            print("Invalid attribute, updates habit_name or periodicity only")
            return

        self.cur.execute(
            f"UPDATE habits_tables SET {attribute} = ? WHERE habit_name = ? ", (value, habit_name)
        )
        self.db.commit()
        print(f" '{habit_name}' updated successfully {attribute} set to {value}")



    """Delete habits"""
    def delete_habit(self, habit_name):
        self.cur.execute(" DELETE FROM habits_tables WHERE habit_name = ?", (habit_name,))

        self.db.commit()




