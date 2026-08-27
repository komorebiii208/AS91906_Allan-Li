# Guess Game (v4 Database Version)

A Tkinter-based quiz game application integrated with SQLite database for user authentication, dynamic game loading, and score persistence.

## Requirements
 - Python 3.14 (64bit)
 - Pillow (`pip install Pillow`)

## Project Structure

v4_database/
│── __pycache__/
│── data/
│   └── guess_game.db
│── image/
│   └── icon.ico
│── database.py
│── v4_game.py
│── v4_main.py
└── README.md

## OOP Design

| Class | Attributes | Key Methods |
|-------|------------|-------------|
| **GuessGameApp** | `root`, `current_user`, `highest_score`, `total_score`, `latest_game_score`, `current_page`, `search_entry` | `__init__()`, `show_page()`, `navigationbar()`, `perform_search()`, `set_active_user()`, `update_user_score()`, `run()` |

| **MainMenu** | `show_page`, `cards_list` | `build_page()`, `game_card()`, `filter_games()`, `start_independent_game()` |

| **Login** | `show_page`, `root`, `app`, `username_entry`, `password_entry` | `user_name()`, `password()`, `button()`, `login_user()`, `sign_up_user()` |

| **Account** | `root`, `show_page`, `app` | `user_name()`, `highest_score()`, `total_score()`, `show_latest_score()` |

| **Game** | `parent`, `game_id`, `data_service`, `questions_list`, `current_index`, `score`, `option_buttons` | `question_area()`, `options_area()`, `footer_area()`, `load_question()`, `check_answer()`, `next_question()`, `show_game_over()`, `on_close()` |

| **GameDataService** | None | `get_questions_for_game()` |

## Database Schema

### `users` Table
Stores user account credentials and aggregate score records.
- **id**: `INTEGER` (PRIMARY KEY, AUTOINCREMENT)
- **username**: `TEXT` (NOT NULL, UNIQUE)
- **password**: `TEXT` (NOT NULL)
- **highest_score**: `INTEGER` (DEFAULT 0)
- **total_score**: `INTEGER` (DEFAULT 0)

### `games` Table
Stores available quiz game categories displayed on the main menu.
- **id**: `INTEGER` (PRIMARY KEY, AUTOINCREMENT)
- **title**: `TEXT` (NOT NULL)
- **cover_color**: `TEXT` (DEFAULT '#1a6fa1')

### `questions` Table
Stores questions associated with specific games.
- **id**: `INTEGER` (PRIMARY KEY, AUTOINCREMENT)
- **game_id**: `INTEGER` (FOREIGN KEY referencing `games(id)`)
- **question_text**: `TEXT` (NOT NULL)
- **option_a**: `TEXT` (NOT NULL)
- **option_b**: `TEXT` (NOT NULL)
- **option_c**: `TEXT` (NOT NULL)
- **option_d**: `TEXT` (NOT NULL)
- **correct_answer**: `TEXT` (NOT NULL)

### `game_records` Table
Tracks game history and individual scores.
- **id**: `INTEGER` (PRIMARY KEY, AUTOINCREMENT)
- **username**: `TEXT` (NOT NULL)
- **game_id**: `INTEGER` (NOT NULL)
- **score**: `INTEGER` (NOT NULL)
- **timestamp**: `TEXT` (NOT NULL)

## Business Rules

1. **User Authentication & Session**:
   - New users can register with a unique username and password. Existing users can log in with valid credentials.
   - The app tracks the active user (`current_user`). If no user is logged in, default score operations fall back to "Default User".

2. **Dynamic Game & Question Loading**:
   - Game cards on the main menu are fetched dynamically from the `games` table in SQLite.
   - Questions and options are retrieved directly from the `questions` table using `game_id`.

3. **Scoring & Leaderboard System**:
   - Each correct answer awards **10 points**.
   - Upon finishing a game, the record is saved to `game_records` with a timestamp.
   - The user's `total_score` accumulates across all games, and `highest_score` updates if the new score exceeds the existing high score.

4. **Search & Navigation**:
   - Typing in the navigation bar search entry filters visible game cards on the Main Menu.
   - Closing a game window restores and displays the main menu window.