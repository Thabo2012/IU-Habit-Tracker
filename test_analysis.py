
import sqlite3
from tracker_analysis import*
from tracker_class import Habit
from main import list_habits
from db_tracker import DBHandler
import pytest
from datetime import datetime, date

db = DBHandler("main.db")
print(hasattr(db, "cur"))
"""All tests are testing using data stored in the DB,"""
class TestTracker:
    """setup and tear down method for cleaning and setup before test"""
    def setup_method(self):
        self.db_handler = DBHandler("main.db")
        self.db = self.db_handler.db
        self.cur = self.db_handler.cur


    def teardown_method(self):
        self.db.close()


    def test_longest_habit_streak(self):
        """Test the longest streak method"""
        self.cur.execute("SELECT habit_name FROM habits_tables LIMIT 1")
        habit = self.cur.fetchone()
        assert habit, "No habits found in database"
        habit_name = habit[0]
        longest_streak = longest_habit_streak(self.db, habit_name)
        assert longest_streak is not None

    def test_missed_habit_days(self):
        """Test missed days"""
        result = missed_habit_days(self.db_handler, "pray for 15 minutes")

    def test_highest_streak_habits(self):
        """Test highest_streak_habits with predefined habits"""
        result = highest_streak_habits(db)
        for period in ["daily", "weekly", "monthly"]:
            if result.get(period):
                habit = result[period]["habit"]
                streak = result[period]["streak"]
                assert habit in [h[0] for h in list_habits(db)]  #habit should exist in DB
                assert streak >= 0

    def test_all_current_streaks(self):
        """Test all current streak"""
        results = all_current_streaks(db)
        for habit_name, streak, periodicity in results:
            assert streak >= 0  # streaks always positive
            assert periodicity.lower() in ["daily", "weekly", "monthly"]

    def test_log_count(self):
        """Log testing for all habits"""

        results = get_log_counts(self.db)
        assert len(results), 1
        habit_name, periodicity, date_created, log_count, _ = results[0]

        assert log_count > 0

    @pytest.mark.parametrize("periodicity", ["daily", "weekly", "monthly"])
    def test_habit_names_periodicity(self, periodicity):
        """Test habits periodicity>>weekly,daily or monthly"""

        result = get_habit_names_periodicity(db, periodicity)

        cur = db.cursor()
        cur.execute(
            "SELECT habit_name FROM habits_tables WHERE LOWER(TRIM(periodicity)) = ?",
            (periodicity.lower().strip(),)
        )
        db_habits = [row[0] for row in cur.fetchall()]

        result_lower = [h.lower() for h in result]
        db_habits_lower = [h.lower() for h in db_habits]

        for habit_name in result_lower:
            assert habit_name in db_habits_lower, f"Habit '{habit_name}' does not exist in DB for periodicity '{periodicity}'"

        assert set(result_lower) == set(db_habits_lower)

    def test_get_logs_for_habit_id(self):
        """Test if a habit id returns the correct logs"""
        result = get_logs_for_habit_id(self.db, 1)
        cur = self.db.cursor()
        cur.execute("SELECT date_completed FROM completion WHERE habit_id = ? ORDER BY date_completed", (1,))
        expected_results = [datetime.fromisoformat(row[0]).date() for row in cur.fetchall()]
        assert result == expected_results


    def test_habit_completion(self):
        """Test if completing a habit in the database records a log"""
        habit_id = 1
        cur = self.db.cursor()
        today = date.today().isoformat() #logs for the today
        cur.execute(
            "INSERT INTO completion (habit_id, date_completed) VALUES (?, ?)",
            (habit_id, today)
        )
        self.db.commit()

        # check if log was added
        cur.execute("SELECT date_completed FROM completion WHERE habit_id = ?", (habit_id,))
        rows = cur.fetchall()
        assert len(rows) > 0
        """The last row has today's date"""
        last_completion = datetime.fromisoformat(rows[-1][0]).date()
        assert last_completion == date.today()




















































