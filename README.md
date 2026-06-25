# Pip

> [!WARNING]
> **Source Available Project**
>
> Pip is licensed under the [**Pip Source Available License (PSAL)**](?tab=readme-ov-file).
>
> ✅ View source code
> ✅ Fork to contribute via pull requests
> ❌ Commercial use
> ❌ Production use without permission
> ❌ Redistribution of modified or unmodified copies
>
> Please read the [LICENSE](https://github.com/FreeSpinner09/PipBot?tab=License-1-ov-file) before using this project.

---

## Overview

Pip is a modern, modular Discord moderation framework built with **discord.py** and **SQLAlchemy**.

Unlike traditional moderation bots that tightly couple commands, database logic, and Discord API interactions, Pip is designed around a layered architecture that separates responsibilities into dedicated components.

The goal is to provide a maintainable, scalable moderation platform capable of supporting:

* Manual moderation
* Automatic moderation
* Heat-based punishments
* AI-assisted moderation
* Future web dashboard integration
* Plugin-friendly architecture

---

# Current Features

## Moderation

* ✅ Warn users
* ✅ Heat system
* ✅ Automatic threshold evaluation
* ✅ Automatic punishment execution
* ✅ Moderation history
* ✅ Individual case lookup

Commands:

```text
/warn
/heat
/history
/case
```

---

## Health

Built-in diagnostics.

```text
/health
```

Displays:

* Database connectivity
* Discord latency
* Loaded cogs
* Cached users
* Connected guilds

---

## Heat System

Each warning contributes configurable **points**.

Points accumulate into a user's **heat**.

Example:

```text
Warn #1
5 Points

Warn #2
10 Points

Current Heat
15
```

Heat determines when automatic punishments occur.

---

## Threshold Engine

Pip automatically evaluates moderation thresholds after every warning.

Example:

```text
25 Heat
↓
Warn

50 Heat
↓
Timeout

100 Heat
↓
Kick

150 Heat
↓
Ban
```

Thresholds are evaluated from highest to lowest.

---

## Automatic Punishments

Once a threshold is reached, Pip automatically executes the configured punishment.

Supported:

* Warn
* Timeout
* Kick
* Ban

---

# Architecture

Pip follows a layered architecture.

```text
Discord Commands
        │
        ▼
      Cogs
        │
        ▼
    Services
        │
        ▼
     Engines
        │
        ▼
    Executors
        │
        ▼
      Database
```

---

## Services

Responsible for business operations and database interactions.

Current services:

* UserService
* CaseService
* WarnService
* ThresholdService
* GuildConfigService
* ModLogService

---

## Engines

Responsible for making decisions.

Current engines:

* ModerationEngine

Example:

```text
Heat
↓
Threshold Evaluation
↓
Recommended Punishment
```

---

## Executors

Responsible for carrying out actions.

Current executors:

* PunishmentExecutor

Example:

```text
Timeout User
Kick User
Ban User
```

Executors do not contain business logic.

---

## Utilities

Shared helpers used throughout the project.

Current utilities include:

* EmbedFactory
* Logger
* Error Handler
* Configuration

---

# Technology Stack

* Python 3.14+
* discord.py
* SQLAlchemy
* SQLite (development)
* dotenv

---

# Project Structure

```text
pip/
│
├── cogs/
├── database/
│   ├── models/
│   └── init_db.py
│
├── services/
├── engines/
├── executors/
├── utils/
│
└── bot.py
```

---

# Roadmap

## MVP

### Core

* [x] Database
* [x] Models
* [x] Services
* [x] Engines
* [x] Executors

### Moderation

* [x] Warn
* [x] Heat
* [x] History
* [x] Case Lookup
* [ ] Warning Management
* [ ] Warning Expiration

### Configuration

* [ ] Threshold Commands
* [x] Configuration Commands
* [ ] Mod Log Channel

### Logging

* [ ] Discord Mod Logs
* [ ] EmbedFactory Integration

### Automod

* [ ] Rule Engine
* [ ] Spam Detection
* [ ] Invite Detection
* [ ] Mention Spam
* [ ] Link Filters

---

## Future

* AI Moderation
* Appeals
* Dashboard
* Analytics
* Web Panel
* Plugin System
* Metrics
* Multi-Database Support

---

# Philosophy

Pip is built around one core principle:

> Every component should have exactly one responsibility.

Services manage data.

Engines make decisions.

Executors perform actions.

Utilities provide reusable functionality.

This separation keeps the project scalable and easy to maintain.

---

# Contributing

Contributions are welcome through pull requests.

Before opening a pull request:

* Follow the existing project architecture.
* Keep business logic out of Discord cogs.
* Keep Discord API interactions inside executors where appropriate.
* Write clean, typed Python code.
* Keep responsibilities separated.

Please note that this project is **source available**, not open source. By contributing, you agree to the terms outlined in the project's [`LICENSE`](https://github.com/FreeSpinner09/PipBot?tab=License-1-ov-file).

---

# License

This project is licensed under the [**Pip Source Available License (PSAL)**](https://github.com/FreeSpinner09/PipBot?tab=License-1-ov-file).

See the [LICENSE](https://github.com/FreeSpinner09/PipBot?tab=License-1-ov-file) file for complete terms and conditions.
