# IU INTERNATIONAL University: Habit Tracker App (DLBDSOOFPP01)

## Overview
A Python based project app that tracks the user habits over daily or weekly period.
Users are able to check their progress, missed days and streaks for analytic purposes.
# Features
- List all habits
- Includes predifined habits
- Create, delete, habits
- Habits completion with timestamp
- Calculate current and target streaks
- Analytical features
  - Missed day
  - Habit longest streak
  - Longest streak for all habits based on periodicity
  - Current streak per periodicity
- Python command line interface(CLI)
- SQlite3 database storage
- Unit test- pytest

## Installations
To start and run the habit tracker app
- Clone the repository: git clone https://github.com/Thabo2012/IU-Habit-tracker
- pip install -r requirements.txt

## Usage
- Run python3 or above. Run main.py to start the CLI
- Foloow the instruction on the "menu screen" and choose one of the choices
- Example
  - List habits
  - Create new habits
  - Complete habits
  - Show longest streak for a habit
  - Exit


## Tests

Run pytest . Start the testing functions included in the modules and classes

# App/project structure

├── main.py --- CLI for user interaction

├── tracker_class.py --- contains a single tracker objects

├── db_tracker.py -- SQLite database storage

├── tracker_analysis -- contains functions to analyse the user performance

├── Unit test--- test unit functions

│ ├── test_analysis.py --- Test analytical functions

│ └── test_tracker.py --- Test module functions, excluding analytics

├── tracker_requirements.txt --- list all tools to build the tracker

└── README.md --- include all documentation of the tracker app










