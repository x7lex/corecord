# Corecord Bot 🤖

Corecord is designed to be the backbone of any modern Discord bot, designed for simplicity, flexibility, and ease of extension.

---

## 📁 Project Structure

```
.
├── bot.py
├── modules/
│   └── example.py
└── utils/
    ├── check_config.py
    ├── check_permissions.py
    ├── colours.py
    └── console.py
```

---

## 📝 File Overview

### `bot.py`

The main entry point of the bot. Handles:

* Client initialization
* Command tree setup
* Dynamic module loading
* Error handling
* Console logging with colors

### `modules/`

Contains all bot commands and logic, automatically loaded at startup. See notes for more details.

* `example.py` – *This is an example command to great via /hello*

### `token.env`

Environment file containing your bot token and other sensitive variables.
⚠️ Keep this file private and never push it to public repositories.

### `utils/`

Helper modules used throughout the bot:

* `check_config.py` – Configuration validation and settings management.

* `check_permissions.py` – Functions for checking permissions and handling command errors.

* `colours.py` – Defines the `Colour` enum for consistent color references (`RED`, `GREEN`, `YELLOW`, `BLUE`).

* `console.py` – Handles logging to the console using colors from `Colour`.

---

## 🚀 Getting Started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Make any .env file and add your Discord bot token:

```
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
```

3. Run the bot:

```bash
python bot.py
```

---

## ⚙️ Adding Modules

1. Create a new file in `modules/`.
2. Define a `register(bot)` function that adds commands or features.
3. The bot will automatically load it on startup.

---

## 🌈 Logging

All logs are printed with colors using the `Colour` enum for easy yet comprehensive debugging:

* `RED` – Errors ❌
* `GREEN` – Success ✅
* `YELLOW` – Warnings ⚠️
* `BLUE` – Info ℹ️

---

## ✨ Contributing

Feel free to fork, add modules, or improve utilities!
Make sure to follow Python best practices and test your changes.

---

## 📌 Notes

* Modules should always have a `register(bot)` function.
* The bot dynamically loads any `.py` file in `modules/` not in `utils/`.
* This was made in Python 3.13 making it the recommended version. 
