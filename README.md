# Automaton Simulator (on Telegram)

This is a Telegram bot that can simulate a finite automaton.

## Table of Contents

- [Automaton Simulator (on Telegram)](#automaton-simulator-on-telegram)
  - [Table of Contents](#table-of-contents)
  - [Usage](#usage)
  - [Environment Variables](#environment-variables)
  - [Database Structure](#database-structure)
  - [License](#license)


## Usage

1. Clone the repository.
2. Create a bot using [@BotFather](https://t.me/BotFather).
3. Copy the token and paste it in the `TG_ACCESS_TOKEN` variable in the [.env.example] file.
4. Fill in the other optional variables in the [.env.example] file.
5. Run by `python src/main.py`.

## Environment Variables

This part describes the environment variables that can be used in the [.env.example] file.

| Variable | Description | Optional? |
| --- | --- | --- |
| `TG_ACCESS_TOKEN` | The access token of the bot. | No |
| `TG_ADMIN_ID` | The Telegram ID of the admin. | Yes |
| `TG_ADMIN_PASSWORD` | The Password used to cause a graceful shutdown from the bot itself. | Yes |
| `DB_HOST` | The host of the database. | Yes |
| `DB_PORT` | The port of the database. | Yes |
| `DB_USER` | The user of the database. | Yes |
| `DB_PASS` | The password of the database. | Yes |
| `DB_NAME` | The name of the database. | Yes |

Not configuring `TG_ADMIN_*` variables will disable the graceful shutdown feature.

Not configuring `DB_*` variables will disable the database feature.

## Database Structure

Skip this section if you don't want to use the database feature.

The database that this project is setup for is MySQL/MariaDB.

Database Diagram:

![Database Diagram](/assets/database_diagram.png)

## License

This project is licensed under the Unlicense. See the [LICENSE] file for details.

[LICENSE]: /LICENSE
[.env.example]: /.env.example
