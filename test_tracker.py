from db_tracker import DBHandler
from main import Habit, list_habits
from tracker_analysis import *
from db_tracker import *

db =  DBHandler("main.db")

"""All tests are testing using data stored in the DB"""
def test_list_habits():
    """Test the list function for listing all habits in database"""
    results = list_habits(db)
    assert results, "No habits found in the database"

def test_habits_str():
    """Test habit object """
    habit = Habit(
        habit_name="read a book",
        periodicity="daily",
        date_created=date.today(),
        logs=["2025-08-25", "2025-08-26"],
        current_streak=3,
        target_streak=5
    )
    assert habit.habit_name == "read a book"


def test_habit_exists():
    """Test that habit in the database exists"""
    results = list_habits(db)
    assert results, "No habits found in the database"

    first_habit = results[0]
    habit_name = first_habit[0]
    print(f"Testing existence of habit: {habit_name}")
    assert db.habit_exists(habit_name) is True

def test_create_new_habit():
    """Test the creation of new habit"""
    habit_name = "Test Habit"
    periodicity = "daily"

    # if habit already exists cleanup
    if db.habit_exists(habit_name):
        db.delete_habit(habit_name)

    db.add_habits_into_tables(Habit(habit_name, periodicity, "2025-08-29"))
    assert db.habit_exists(habit_name) is True

    # after test clean up
    db.delete_habit(habit_name)


def test_delete_habit():
    """Delete habits if it exists"""
    habit_name = "Temp Habit"
    periodicity = "daily"

    if not db.habit_exists(habit_name):
        db.add_habits_into_tables(Habit(habit_name, periodicity, "2025-08-29"))

    db.delete_habit(habit_name)
    assert db.habit_exists(habit_name) is False


def test_update_habit():
    """Test the update methods for habits"""
    habit_name = "Update Habit"
    db.add_habits_into_tables(Habit(habit_name, "daily", "2025-08-29"))

    #updating name
    db.update_habit(habit_name, "habit_name", "Updated Habit")
    assert db.habit_exists("Updated Habit") is True

    # periodicity update
    db.update_habit("Updated Habit", "periodicity", "weekly")
    db.delete_habit("Updated Habit")


