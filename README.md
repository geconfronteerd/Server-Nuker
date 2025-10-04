# Discord Moderation Bot

A simple Discord bot built with [discord.py](https://discordpy.readthedocs.io/) for server moderation tasks such as deleting messages, channels, and roles.

---

## Features

* **Delete Messages**
  `!delmsg <amount>` – Delete a specified number of messages (1–100).

* **Delete All Channels**
  `!delchannel` – Delete all channels in the server. *(Requires `Manage Channels` permission).*

* **Delete All Roles**
  `!delrole` – Delete all roles in the server except `@everyone`. *(Requires `Manage Roles` permission).*

* **Nuke Server**
  `!nuke` – Delete **all channels and roles** in the server. *(Requires both `Manage Channels` and `Manage Roles` permissions).*

* **Help Command**
  `!help_mod` – Displays available moderation commands in an embed.

---

## Requirements

* Python 3.8+
* [discord.py](https://pypi.org/project/discord.py/) library

Install dependencies with:

```bash
pip install discord.py
```

---

## Setup

1. Clone or download this repository.
2. Create a `config.json` file in the root directory with your bot token:

```json
{
  "token": "your_bot_token_here"
}
```

3. Run the bot:

```bash
python bot.py
```

---

## Permissions Needed

For the bot to function properly, make sure it has:

* **Manage Messages** (for deleting messages)
* **Manage Channels** (for deleting channels)
* **Manage Roles** (for deleting roles)

---

## ⚠️ Important Warning

* The `!nuke`, `!delchannel`, and `!delrole` commands are **destructive** and cannot be undone.
* Use these commands with extreme caution.

---

## Example Usage

* `!delmsg 10` → Deletes the last 10 messages in a channel.
* `!delchannel` → Deletes all channels.
* `!delrole` → Deletes all roles except `@everyone`.
* `!nuke` → Completely wipes out channels and roles.
* `!help_mod` → Shows command help.

---

## License

This project is open-source and available under the MIT License.
