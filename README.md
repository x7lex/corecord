# 🤖 CoreCord
CoreCord is the foundation for any Discord bot, offering helpful utilities that make bot development simpler and more user-friendly.
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
> ℹ️ You are required to create a `.env` file (or any name you prefer) in your project.  
> Then add the following environment variable:
> `DISCORD_TOKEN`

---

## 📝 File Overview

### `bot.py`

The main entry point of the bot. Handles:

* Client initialization
* Command tree setup
* Dynamic module loading
* Error handling

### `modules/`

Contains all bot commands and logic, automatically loaded at startup. See notes for more details.

* `example.py` – *This is an example command to great via* /hello

### `utils/`

Helper modules used throughout the bot:

* `check_config.py` – Configuration validation and settings management.

* `check_permissions.py` – Functions for checking permissions and handling command errors.

* `colours.py` – Defines the `Colour` enum for consistent color references (`RED`, `GREEN`, `YELLOW`, `BLUE`).

* `console.py` – Handles logging to the console using colors from `Colour`.

---
## ✅ Getting Started

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

