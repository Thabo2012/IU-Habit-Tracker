import sqlite3
from datetime import datetime, timedelta, date
from db_tracker import DBHandler



def get_habit_names_periodicity(db, periodicity):
    """Returning a list of habits by periodicity, Daily/Weekly"""
    cur = db.cursor()
    cur.execute("SELECT habit_name FROM habits_tables "
                "WHERE lower(periodicity) = ?", (periodicity.lower(),))
    return [row[0].lower() for row in cur.fetchall()]


def habit_completion(db):
    """User to fill in the day or time they completed an activity or one of the habit"""
    cur = db.cursor()
    cur.execute("SELECT id, habit_name, periodicity, target_streak, current_streak FROM habits_tables")
    habits = cur.fetchall()

    if not habits:
        print("No habits found.")
        return
    # if the habit id is not available, user will be prompt to enter
    print("\nAvailable habits:")
    for h in habits:
        print(f"{h[0]}. {h[1].title()} ({h[2]}, Goal: {h[3]}, Current: {h[4]})")

    """Choose the desired habit"""
    while True:
        try:
            habit_id = int(input("\nEnter the habit ID to log: "))
            habit = next((h for h in habits if h[0] == habit_id), None)
            if habit:
                break
            print("Invalid ID.")
        except ValueError:
            print("Enter a number.")

    habit_name, periodicity, target, current = habit[1], habit[2], habit[3], habit[4]

    """log date completion manually"""
    while True:
        date_input = input("Enter date completed (YYYY-MM-DD) or 'today': ").strip().lower()
        if date_input == "today":
            log_date = date.today().isoformat()
            break
        try:
            log_date = datetime.strptime(date_input, "%Y-%m-%d").date().isoformat()
            break
        except ValueError:
            print("Invalid date format.")


    """Prevents duplicating logs"""

    cur.execute("SELECT 1 FROM completion WHERE habit_id = ? AND date(date_completed) = ?", (habit_id, log_date))
    if cur.fetchone():
        print("\u26a0\ufe0f Already logged for that date.")
        return

    """Insert the new log completion"""

    cur.execute("INSERT INTO completion (habit_id, date_completed) VALUES (?, ?)", (habit_id, log_date))
    db.commit()

    """# Update the current streak"""
    new_streak = (current or 0)+ 1
    cur.execute("UPDATE habits_tables SET current_streak = ? WHERE id = ?", (new_streak, habit_id))
    db.commit()

    print(f"Logged '{habit_name}' for {log_date}. Current streak: {new_streak}/{target}")

    if new_streak >= (target or 7):
        print(f"You reached your goal of {target} for '{habit_name}'!")

def all_current_streaks(db):
    """Return current streak for all habits in completion table"""
    cur = db.cursor()
    cur.execute("SELECT id, habit_name, periodicity FROM habits_tables")
    habits = cur.fetchall()

    results = []

    for habit_id, name, periodicity in habits:
        # get the completed date
        cur.execute("""
                SELECT date_completed
                FROM completion
                WHERE habit_id = ?
                ORDER BY date_completed DESC
            """, (habit_id,))
        raw_dates = [row[0] for row in cur.fetchall()]

       # datetime conversion
        dates = []
        for d in raw_dates:
            try:
                dates.append(datetime.fromisoformat(d.strip()).date())
            except ValueError:
                continue

        # streak calculation
        streak = 0
        if dates:
            streak = 1
            for i in range(1, len(dates)):
                diff_days = (dates[i - 1] - dates[i]).days

                if periodicity.lower() == "daily" and diff_days == 1:
                    streak += 1
                elif periodicity.lower() == "weekly" and diff_days <= 7:
                    streak += 1
                elif periodicity.lower() == "monthly" and (
                        (dates[i - 1].year == dates[i].year and dates[i - 1].month - dates[i].month == 1)
                        or (dates[i - 1].month == 1 and dates[i].month == 12 and dates[i - 1].year - dates[i].year == 1)
                ):
                    streak += 1
                else:
                    break

        results.append((name, streak, periodicity))
    #optional print in CLI
    print("Current Streaks:")
    for habit_name, streak, periodicity in results:
        print(f"- {habit_name}: {streak}: {periodicity}")

    return results

def get_log_counts(db):
    """Return a summary of habits in the habit tracker app"""
    cur = db.cursor()
    cur.execute(
        """SELECT h.id, h.habit_name, h.periodicity, h.date_created, COUNT(c.id) AS log_counts
            FROM habits_tables h
            LEFT JOIN completion c ON h.id = c.habit_id
            GROUP BY h.id, h.habit_name, h.periodicity, h.date_created
            """)
    results = []
    rows = cur.fetchall()

    for habit_id, habit_name,periodicity, date_created, log_counts in rows:
            cur.execute(
            "SELECT date_completed FROM completion WHERE habit_id = ? ORDER by date_completed",(habit_id,)
            )

            dates = [datetime.fromisoformat(row[0]).date() for row in cur.fetchall()]

            longest = 1 if dates else 0
            current = 1

            gap = timedelta(days =1) if periodicity == "daily"  else timedelta(weeks = 1)

            for i in range(1, len(dates)):
                if dates[i] - dates[i - 1] == gap:
                    current += 1
                    longest = max(longest, current)
                else:
                    current = 1

            results.append((habit_name, periodicity, date_created, log_counts, longest))

    return results

def get_logs_for_habit_id(db, habit_id):
    """Returning the completion dates for a specific habit"""
    cur = db.cursor()
    cur.execute("SELECT date_completed FROM completion WHERE habit_id = ? ORDER BY date_completed", (habit_id,))
    return [datetime.fromisoformat(row[0]).date() for row in cur.fetchall()]



def longest_habit_streak(db, habit_name):
    """Calculate the longest streak of a habit"""
    cur = db.cursor()
    cur.execute("SELECT id, periodicity FROM habits_tables WHERE LOWER(habit_name) = LOWER(?)", (habit_name,))
    result = cur.fetchone()

    if not result:
        print(f"Habit '{habit_name}' not found.")
        return 0


    habit_id, periodicity = result
    dates = get_logs_for_habit_id(db, habit_id)

    if not dates or len(dates) < 2:
        return 1 if dates else 0

    dates.sort()
    expected_gap = timedelta(days=1) if periodicity == "daily" else timedelta(weeks=1)
    grace_period = timedelta(hours=12) if periodicity == "daily" else timedelta(days=1)

    longest = current = 1

    for i in range(1, len(dates)):
        if abs((dates[i] - dates[i - 1]) - expected_gap) <= timedelta(hours=12):
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest



def highest_streak_habits(db):
    """Calculate the highest streak of all habits"""
    cur = db.cursor()
    cur.execute("SELECT habit_name, periodicity FROM habits_tables")
    habits = cur.fetchall()

    highest_daily = {"habit": None, "streak": 0}
    highest_weekly = {"habit": None, "streak": 0}

    for habit_name, periodicity in habits:
        # Fetching the highest daily/weekly streak of all habit
        streak = longest_habit_streak(db, habit_name)

        if periodicity.lower() == "daily" and streak > highest_daily["streak"]:
            highest_daily["habit"] = habit_name
            highest_daily["streak"] = streak

        elif periodicity.lower() == "weekly" and streak > highest_weekly["streak"]:
            highest_weekly["habit"] = habit_name
            highest_weekly["streak"] = streak

    print("\n🔥Highest Daily Streak:")
    if highest_daily["habit"]:
        print(f"Habit: {highest_daily['habit']}")
        print(f"Streak: {highest_daily['streak']} days")
    else:
        print("No daily streaks found.")

    print("\n🔥Highest Weekly Streak:")
    if highest_weekly["habit"]:
        print(f"Habit: {highest_weekly['habit']}")
        print(f"Streak: {highest_weekly['streak']} weeks")
    else:
        print("No weekly streaks found.")

    return {
        "daily": highest_daily,
        "weekly": highest_weekly
    }



def missed_habit_days(db,habit_name):
    """Calculate missed days by user"""
    cur = db.cursor()
    cur.execute("SELECT id, habit_name, periodicity, date_created FROM habits_tables WHERE lower(habit_name) = ? ", (habit_name.lower(),))
    habits = cur.fetchone()

    if habits:
        habit_id, habit_name, periodicity, date_created_str = habits
    else:
         print(f"habit {habit_name} not found")
         return

    try:
      date_created = datetime.fromisoformat(date_created_str).date()

    except ValueError:
        print("Invalid date format")
        return

    cur.execute("SELECT date_completed FROM completion WHERE habit_id = ?", (habit_id,))
    completed = {datetime.fromisoformat(row[0]).date()
                 for row in cur.fetchall()}

    missed = []
    today = datetime.now().date()
    current = date_created

    while current <= today:
        if current not in completed:
            missed.append(current)
        current += timedelta(days=1) if periodicity == "daily" else timedelta(weeks=1)


    print(f"Days missed for {habit_name} : {[d.strftime('%Y-%m-%d') for d in missed]}")
    return missed



