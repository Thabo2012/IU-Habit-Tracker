import sqlite3
from tracker_class import Habit
from tracker_analysis import (get_log_counts, get_habit_names_periodicity,longest_habit_streak, highest_streak_habits, all_current_streaks,habit_completion,
                              missed_habit_days)
from db_tracker import DBHandler
from datetime import datetime, timedelta

"""The Predefined habits that I added in main instead of DB"""
HABIT_TYPE = [
    Habit(
        "Pray for 15 minutes",
        "Daily",
        "2025-07-01T07:00:00",
        logs=["2025-07-01T07:00:00", "2025-07-02T07:00:00", "2025-07-03T07:00:00", "2025-07-04T07:00:00",
              "2025-07-05T07:00:00", "2025-07-06T07:00:00",
              "2025-07-07T07:00:00", "2025-07-08T07:00:00", "2025-07-09T07:00:00", "2025-07-10T07:00:00",
              "2025-07-11T07:00:00", "2025-07-12T07:00:00",
              "2025-07-13T07:00:00", "2025-07-14T07:00:00", "2025-07-15T07:00:00", "2025-07-16T07:00:00",
              "2025-07-17T07:00:00", "2025-07-18T07:00:00",
              "2025-07-19T07:00:00", "2025-07-20T07:00:00", "2025-07-21T07:00:00", "2025-07-22T07:00:00",
              "2025-07-23T07:00:00",
              "2025-07-25T07:00:00", "2025-07-26T07:00:00", "2025-07-27T07:00:00", "2025-07-28T07:00:00"],
        current_streak = 4,
        target_streak = 14
    ),

    Habit(
        "Walk 2000 steps",
        "Daily",
        "2025-07-01T08:00:00",
        logs=["2025-07-01T08:00:00", "2025-07-02T08:00:00", "2025-07-03T08:00:00", "2025-07-04T08:00:00",
              "2025-07-05T08:00:00", "2025-07-06T08:00:00",
              "2025-07-07T08:00:00", "2025-07-08T08:00:00", "2025-07-09T08:00:00", "2025-07-10T08:00:00",
              "2025-07-11T08:00:00", "2025-07-12T08:00:00",
              "2025-07-13T08:00:00", "2025-07-14T08:00:00", ],
        current_streak = 14,
        target_streak = 14
),

    Habit(
        "Read a book",
        "Daily",
        "2025-07-01T09:00:00",
        logs=["2025-07-01T09:00:00", "2025-07-02T09:00:00", "2025-07-03T09:00:00", "2025-07-04T09:00:00",
              "2025-07-05T09:00:00", "2025-07-06T09:00:00",
              "2025-07-08T09:00:00", "2025-07-09T09:00:00", "2025-07-10T09:00:00",
              "2025-07-11T09:00:00", "2025-07-12T09:00:00",],

        current_streak = 5,
        target_streak = 14
    ),

    Habit(
        "Clean the yard",
        "Weekly",
        "2025-07-04T17:00:00",
        logs=["2025-07-04T17:00:00", "2025-07-11T17:00:00", "2025-07-13T17:00:00", "2025-01-14T17:00:00"],
        current_streak = 2,
        target_streak = 7
),

    Habit(
        "Wash the dog",
        "Weekly",
        "2025-07-03T18:00:00",
        logs=["2025-07-03T18:00:00", "2025-07-04T18:00:00", "2025-07-05T18:00:00", "2025-07-06T18:00:00",
              "2025-07-07T18:00:00","2025-07-08T18:00:00","2025-07-09T18:00:00"],
        current_streak = 7,
        target_streak=7
    ),
]

def list_habits(db):
    """Print all habits with logs"""
    rows = get_log_counts(db)
    if not rows:
        print("No habits found in database.")
    else:
        print("Habit found)")
    for row in rows:
        print(row)
    return rows



def main():
    db = DBHandler()
    db.create_habits_tables()
    db.add_habits_into_tables(HABIT_TYPE)

    """While statement to allow users to choose from the main menu"""
    while True:
        print("==============👣Welcome to Habit tracking app👣===========\n")
        print("☰Choose from the below Menu: ")
        print('1,📱List all habits: ')
        print('2,➕Create new habits:  ')
        print('3,✏️Edit habit: ')
        print('4,✅Complete habit: ')
        print('5,🗑️Delete habits: ')
        print('6,📅Habit periodicity: ')
        print('7,🚫❌Missed days: ')
        print("8,🔥Show current streaks per periodicity")
        print("9,🔗Show longest streak for a habit")
        print("10,🏆Show longest streaks for all habits per periodicity")
        print("11,❌Exit")

        choice = input("Select choice: ")

        if choice == '1':
            logs  = get_log_counts(db)

            for habit_name, periodicity,date_created, count, streak in logs:
                print(f"Habit name: {habit_name}")
                print(f"Created: {date_created}")
                print(f"Periodicity: {periodicity}")
                print(f"Log counts: {count}")
                print(f"Streak: {streak}")
                print("-" * 25)

        elif choice == '2':
            db.create_new_habit()

        elif choice == '3':
            habit_name = input("Enter habit to edit: ").strip().lower()
            if not db.habit_exists(habit_name):
                print("Invalid habit back to Main menu")
            new_habit_name = input("New habit name: ").strip().lower()
            new_habit_periodicity = input("New period(daily/weekly): ").strip().lower()

            if new_habit_name:
                db.update_habit(habit_name, "habit_name", new_habit_name)
                habit_name = new_habit_name

            if new_habit_periodicity in ("daily", "weekly"):
                db.update_habit(habit_name, "periodicity", new_habit_periodicity)

            else:
                print("Habit not updated, invalid choice")


        elif choice == "4":
            habit_completion(db)


        elif choice == '5':
            habit_name = input("Enter name of the habit you want to delete: ").strip().lower()
            if not db.habit_exists(habit_name):
                print("Invalid habit, back to Main Menu\n")
                continue
            confirm = input(f"if you are sure you want to delete {habit_name} type  'yes' to confirm: ").strip().lower()
            if confirm == "yes":
                db.delete_habit(habit_name)
                print(f" Habit---> {habit_name} is deleted\n")
            else:
                print("Invalid choice, please select option 1-->4\n")

        elif choice == '6':
            """Return Daily/Weekly habits"""
            daily = get_habit_names_periodicity(db, "daily")
            weekly = get_habit_names_periodicity(db, "weekly")

            print("Daily Habits")

            if daily:
                for habits in daily:
                    print(habits)

            else:
                print("Nothing")
            print("****************************")

            print("Weekly Habits")

            if weekly:
                for habits in weekly:
                    print(habits)
            else:
                print("Nothing")

        elif choice == '7':
            habit_name = input("Enter habit name: ").strip().lower()
            missed_habit_days(db,habit_name)

        elif choice == "8":
            all_current_streaks(db)

        elif choice == "9":
            habit_name = input("Enter habit name: ").strip().lower()
            print(f"Looking for habit: '{habit_name}'")
            streak = longest_habit_streak(db, habit_name)
            if streak == 0:
                print(f"No completion records found for habit '{habit_name}'.")
            else:
                print(f"Longest streak for '{habit_name}': {streak}")


        elif choice == "10":
            highest_streak_habits(db)

        elif choice == "11":
            print("Goodbye!")

            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
