# Modmail + Moderation Bot

A modular, plugin-based Discord bot built on [Eris](https://abal.moe/Eris/) for handling modmail, auto-moderation, and thread-based communication between staff and users via DMs.

---

## 🚀 Features

- 📬 **Modmail Threading**: Receive user DMs, open threads, log all messages, and let staff reply from a channel.
- 🧩 **Plugin System**: Easily add or remove core functionality like closing threads, blocking users, logging, and more.
- 📄 **Configurable Behavior**: Set your status, command aliases, and server-specific behavior from the config.
- 👮 **Owner-only Commands**: Admin tools to inspect and manage servers the bot is in.
- 🔄 **Persistent**: Built to run continuously via Docker, with `--restart=always` support.
- 🧠 **Database-Backed**: Uses Knex.js for thread, message, and log storage.

---

## ⚙️ Installation

Clone the repo and install dependencies:

```bash
npm install
