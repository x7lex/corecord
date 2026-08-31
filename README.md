# Botcore

Botcore provides a foundation for developers to build and customize their own Discord bots without writing an entire base.

Botcore automatically handles the following:

* **Slash Comamnds:** Built in support for creating and managing Discord slash commands.
* **Module Loading:** Automatically imports bot modules. `/src/modules`
* **Logging:** Built in logging with output stored in `/logs`.
* **Permission Handling:** Centralized permission checks and access control.
* **Cog Management:** Built in support for organizing commands and functionality using Discord.py Cogs.

## Setup
MacOS & Linux:

Make the virtual enviorment first:

`python -m venv .venv`

Then depending on your shell, you activate it:

**Bash / Zsh:**

`source .venv/bin/activate`

**Fish:**

`source .venv/bin/activate.fish`

Windows:

`py -m venv .venv`

Then activate it depending on your shell:

**PowerShell:**

`.venv\Scripts\Activate.ps1`

**Command Prompt (CMD):**

`.venv\Scripts\activate.bat`

### Install Dependencies

Once the virtual environment is activated:

`pip install -r requirements.txt`


